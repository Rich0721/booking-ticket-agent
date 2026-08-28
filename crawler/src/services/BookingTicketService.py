from datetime import date
from typing import List, Tuple, Optional, Set
from twocaptcha import TwoCaptcha
from concurrent.futures import ThreadPoolExecutor
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo
from src.objects.classes.CWebDriver import CWebDriver
from src.repositories.BookingTicketRepository import BookingTicketRepository
from src.utils.booking_utils import (
    parse_train_schedules, find_best_train, extract_pnr_code,
    TRAIN_NO_KEY
)

logger = logging.getLogger(__name__)


class BookingTicketService:
    """訂票服務類，負責處理高鐵訂票的主要流程"""
    
    BOOKING_URL = "https://irs.thsrc.com.tw"
    MAX_WORKERS = 3
    RETRY_COUNT = 3
    TWO_CAPTCHA_API_KEY = os.getenv("TWO_CAPTCHA_API_KEY", "")
    SOLVER = TwoCaptcha(TWO_CAPTCHA_API_KEY)
    
    # Driver超時時間設定（秒）
    DRIVER_TIMEOUT_SECONDS = 30.0
    
    def __init__(self):
        self.repository = BookingTicketRepository()
        self.web_driver_manager = CWebDriver.get_instance()
        self.__failed_bookings: List[CBookingTicketInfo] = []
        self.__retry_bookings: Set[int] = set()  # 追蹤已經重試過的booking IDs
    
    def process_daily_bookings(self, booking_date: date) -> Tuple[int, int]:
        """
        處理指定日期的所有訂票
        
        Args:
            booking_date: 可訂票日期
            
        Returns:
            成功訂票數和失敗訂票數
        """
        # 查詢待訂票記錄
        bookings = self.repository.get_booking_tickets_by_can_book_date(booking_date)
        
        if not bookings:
            print(f"沒有找到日期 {booking_date} 的待訂票記錄")
            return 0, 0
        
        print(f"找到 {len(bookings)} 筆待訂票記錄")
        
        # 計算線程數，以3為倍數
        thread_count = min(len(bookings), self.MAX_WORKERS)
        
        # 使用ThreadPoolExecutor進行多線程訂票
        self.__failed_bookings = []
        self.__retry_bookings = set()
        successful_count = 0
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for index, booking in enumerate(bookings):
                future = executor.submit(
                    self._process_single_booking,
                    booking,
                    index,
                    is_retry=False
                )
                futures.append((booking, future))
            
            # 等待所有任務完成
            for booking, future in futures:
                try:
                    success = future.result(timeout=300)
                    if success:
                        successful_count += 1
                    else:
                        self.__failed_bookings.append(booking)
                except Exception as e:
                    logger.error(f"訂票失敗 (ID: {booking.booking_id}): {str(e)}")
                    self.__failed_bookings.append(booking)
        
        # 重試失敗的訂票
        retry_count = 0
        for booking in self.__failed_bookings[:]:  # 使用列表副本以允許修改原列表
            try:
                logger.info(f"開始重試訂票 (ID: {booking.booking_id})")
                self.__retry_bookings.add(booking.booking_id)
                
                success = self._process_single_booking(
                    booking,
                    0,
                    is_retry=True
                )
                
                if success:
                    retry_count += 1
                    self.__failed_bookings.remove(booking)
                    logger.info(f"重試訂票成功 (ID: {booking.booking_id})")
                else:
                    logger.warning(f"重試訂票失敗 (ID: {booking.booking_id})")
            
            except Exception as e:
                logger.error(f"重試訂票異常 (ID: {booking.booking_id}): {str(e)}")
        
        # 標記仍然失敗的訂票
        for booking in self.__failed_bookings:
            logger.warning(f"標記訂票失敗 (ID: {booking.booking_id}) - 狀態: Booking Error")
            self.repository.update_ticket_number(booking.booking_id, "Booking Error")
        
        failed_count = len(self.__failed_bookings)
        return successful_count + retry_count, failed_count
        
    
    def _process_single_booking(
        self,
        booking_info: CBookingTicketInfo,
        thread_id: int,
        is_retry: bool = False
    ) -> bool:
        """
        處理單筆訂票
        
        Args:
            booking_info: 訂票資訊
            thread_id: 線程ID
            is_retry: 是否為重試操作
            
        Returns:
            是否訂票成功
        """
        driver = None
        try:
            driver = self.web_driver_manager.create_driver(enable_timeout=True)
            
            # 設置超時回調
            def on_driver_timeout():
                logger.warning(
                    f"Driver超時 (booking_id: {booking_info.booking_id}, is_retry: {is_retry})"
                )
                if driver:
                    try:
                        driver.quit()
                    except Exception as e:
                        logger.warning(f"關閉超時Driver時發生異常: {str(e)}")
            
            self.web_driver_manager._CWebDriver__timeout_manager.set_timeout_callback(
                on_driver_timeout
            )
            
            # 第一步：訪問訂票網站並接受Cookie
            self._accept_cookie(driver, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 第二步：填寫基本訂票資訊
            self._fill_basic_booking_info(driver, booking_info, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 第三步：解決驗證碼並查詢
            self._handle_captcha_and_search(driver, thread_id, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 等待結果加載
            time.sleep(2)
            
            # 第四步：選擇車次
            html = driver.page_source
            schedules = parse_train_schedules(html)
            
            if not schedules:
                logger.warning(
                    f"訂票 ID {booking_info.booking_id} 找不到可用車次"
                )
                return False
            
            selected_train = find_best_train(
                schedules,
                booking_info.booking_time.strftime("%H:%M"),
                booking_info.is_early_bird
            )
            
            if not selected_train:
                logger.warning(
                    f"訂票 ID {booking_info.booking_id} 無法選擇車次"
                )
                return False
            
            self._select_train(driver, selected_train, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 第五步：填寫訂票人資訊
            time.sleep(1)
            self._fill_booker_info(driver, booking_info, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 第六步：填寫乘客資訊和會員資訊
            self._fill_passenger_and_member_info(driver, booking_info, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 第七步：完成訂票
            time.sleep(1)
            self._submit_booking(driver, booking_info.booking_id)
            self.web_driver_manager.reset_activity()
            
            # 等待結果頁面加載
            time.sleep(2)
            
            # 第八步：提取訂單代號
            html = driver.page_source
            ticket_number = extract_pnr_code(html)
            
            if ticket_number:
                # 更新數據庫
                success = self.repository.update_ticket_number(
                    booking_info.booking_id,
                    ticket_number
                )
                logger.info(
                    f"訂票成功 (ID: {booking_info.booking_id}, 訂單: {ticket_number})"
                )
                return success
            else:
                logger.warning(
                    f"訂票失敗 (ID: {booking_info.booking_id}) - 無法取得訂單代號"
                )
                return False
        
        except Exception as e:
            logger.error(
                f"訂票過程中發生錯誤 (ID: {booking_info.booking_id}, is_retry: {is_retry}): {str(e)}"
            )
            
            # 檢查是否是Driver超時
            if self.web_driver_manager.is_driver_timeout():
                logger.warning(
                    f"Driver超時導致訂票失敗 (ID: {booking_info.booking_id}, is_retry: {is_retry})"
                )
            
            return False
        finally:
            if driver:
                try:
                    self.web_driver_manager.close_driver()
                except Exception as e:
                    logger.warning(f"關閉Driver時發生異常: {str(e)}")
    
    def _accept_cookie(self, driver: webdriver.Edge, booking_id: int) -> None:
        """
        訪問訂票網站並接受Cookie
        
        Args:
            driver: WebDriver實例
            booking_id: 訂票ID（用於日誌）
        """
        driver.get(self.BOOKING_URL)
        time.sleep(1)
        
        try:
            cookie_btn = driver.find_element(By.ID, 'cookieAccpetBtn')
            driver.execute_script("arguments[0].click();", cookie_btn)
            time.sleep(0.5)
        except NoSuchElementException:
            logger.warning(f"未找到Cookie接受按鈕 (booking_id: {booking_id})")
    
    def _fill_basic_booking_info(
        self,
        driver: webdriver.Edge,
        booking_info: CBookingTicketInfo,
        booking_id: int
    ) -> None:
        """
        填寫基本訂票資訊
        
        Args:
            driver: WebDriver實例
            booking_info: 訂票資訊
            booking_id: 訂票ID（用於日誌）
        """
        try:
            # 填寫出發站
            start_select = Select(driver.find_element(By.ID, "BookingS1Form_selectStartStation"))
            start_select.select_by_value(booking_info.start_station)
            time.sleep(0.3)
            
            # 填寫到達站
            end_select = Select(driver.find_element(By.ID, "BookingS1Form_selectDestinationStation"))
            end_select.select_by_value(booking_info.end_station)
            time.sleep(0.3)
            
            # 填寫出發日期
            input_element = driver.find_element(By.ID, "toTimeInputField")
            date_str = booking_info.booking_date.strftime("%Y/%m/%d")
            driver.execute_script(f"arguments[0]._flatpickr.setDate('{date_str}');", input_element)
            time.sleep(0.5)
            
            # 填寫出發時間
            time_input = driver.find_element(By.NAME, "toTimeTable")
            time_str = booking_info.booking_time.strftime("%H:%M")
            time_input.send_keys(time_str)
            time.sleep(0.5)
            # 填寫票種信息
            self._fill_ticket_counts(driver, booking_info, booking_id)
        
        except Exception as e:
            logger.error(
                f"填寫基本訂票資訊失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
    
    def _fill_ticket_counts(
        self,
        driver: webdriver.Edge,
        booking_info: CBookingTicketInfo,
        booking_id: int
    ) -> None:
        """
        填寫各類票型數量
        
        Args:
            driver: WebDriver實例
            booking_info: 訂票資訊
            booking_id: 訂票ID（用於日誌）
        """
        try:
            # 全票
            adult_select = Select(driver.find_element(By.NAME, "ticketPanel:rows:0:ticketAmount"))
            adult_select.select_by_value(str(booking_info.adult_count) + "F")
            time.sleep(0.2)
            
            # 孩童票
            child_select = Select(driver.find_element(By.NAME, "ticketPanel:rows:1:ticketAmount"))
            child_select.select_by_value(str(booking_info.child_count) + "H")
            time.sleep(0.2)

            # 愛心票
            disabled_select = Select(driver.find_element(By.NAME, "ticketPanel:rows:2:ticketAmount"))
            disabled_select.select_by_value(str(booking_info.disabled_count) + "W")
            time.sleep(0.2)

            # 敬老票
            elder_select = Select(driver.find_element(By.NAME, "ticketPanel:rows:3:ticketAmount"))
            elder_select.select_by_value(str(booking_info.elder_count) + "E")
            time.sleep(0.2)

            
            # 大學生票
            student_select = Select(driver.find_element(By.NAME, "ticketPanel:rows:4:ticketAmount"))
            student_select.select_by_value(str(booking_info.student_count) + "P")
            time.sleep(0.2)
           
        except Exception as e:
            logger.error(
                f"填寫票型數量失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
    
    def _handle_captcha_and_search(
        self,
        driver: webdriver.Edge,
        thread_id: int,
        booking_id: int
    ) -> None:
        """
        處理驗證碼並執行查詢
        
        Args:
            driver: WebDriver實例
            thread_id: 線程ID
            booking_id: 訂票ID（用於日誌）
        """
        try:
            # 這裡需要使用2Captcha API進行驗證碼識別
            # 由於沒有提供具體的實現細節，這裡使用占位符

            image_name = f"captcha_{thread_id:05d}.png"
            img_src = driver.find_element(By.ID, "BookingS1Form_homeCaptcha_passCode")
            img_src.screenshot(image_name)
            result = self.SOLVER.normal(image_name)
            driver.find_element(By.ID, "securityCode").send_keys(result['code'].upper())
            os.remove(image_name)
            time.sleep(0.5)

            submit_btn = driver.find_element(By.ID, "SubmitButton")
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(2)
        except Exception as e:
            logger.error(
                f"驗證碼處理失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
    
    def _select_train(
        self,
        driver: webdriver.Edge,
        selected_train: dict,
        booking_id: int
    ) -> None:
        """
        選擇列車
        
        Args:
            driver: WebDriver實例
            selected_train: 選定的列車資訊
            booking_id: 訂票ID（用於日誌）
        """
        try:
            train_no = selected_train.get(TRAIN_NO_KEY)
            radio_btn = driver.find_element(By.CSS_SELECTOR, f"input[querycode='{train_no}']")
            driver.execute_script("arguments[0].click();", radio_btn)
            time.sleep(0.5)
            
            submit_btn = driver.find_element(By.NAME, "SubmitButton")
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(1)
        except Exception as e:
            logger.error(
                f"選擇列車失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
    
    def _fill_booker_info(
        self,
        driver: webdriver.Edge,
        booking_info: CBookingTicketInfo,
        booking_id: int
    ) -> None:
        """
        填寫訂票人資訊
        
        Args:
            driver: WebDriver實例
            booking_info: 訂票資訊
            booking_id: 訂票ID（用於日誌）
        """
        try:
            id_input = driver.find_element(By.ID, "idNumber")
            id_input.send_keys(booking_info.user_id)
            time.sleep(0.5)
        except Exception as e:
            logger.error(
                f"填寫訂票人資訊失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
    
    def _fill_passenger_and_member_info(
        self,
        driver: webdriver.Edge,
        booking_info: CBookingTicketInfo,
        booking_id: int
    ) -> None:
        """
        填寫乘客資訊和會員資訊
        
        Args:
            driver: WebDriver實例
            booking_info: 訂票資訊
            booking_id: 訂票ID（用於日誌）
        """
        try:
            # 填寫早鳥票乘客資訊
            if booking_info.is_early_bird and booking_info.early_bird_ids:
                for idx, passenger_id in enumerate(booking_info.early_bird_ids):
                    passenger_input = driver.find_element(
                        By.ID,
                        f"BookingS3Form_TicketPassengerInfoInputPanel_passengerDataView_{idx}_passengerDataView2_passengerDataIdNumber"
                    )
                    passenger_input.send_keys(passenger_id)
                    time.sleep(0.3)
            
            # 選擇會員選項
            member_radio = driver.find_element(By.ID, 'memberSystemRadio1')
            driver.execute_script("arguments[0].click();", member_radio)
            time.sleep(0.2)
            
            # 如果是會員，填寫會員信息
            if booking_info.is_member:
                member_checkbox = driver.find_element(By.ID, 'memberShipCheckBox')
                driver.execute_script("arguments[0].click();", member_checkbox)
                time.sleep(0.2)
                
                # member_input = driver.find_element(By.ID, "msNumber")
                # member_input.send_keys(booking_info.user_id)
                # time.sleep(0.3)
            
            # 勾選同意條款
            agree_checkbox = driver.find_element(By.NAME, 'agree')
            driver.execute_script("arguments[0].click();", agree_checkbox)
            time.sleep(0.3)
        except Exception as e:
            logger.error(
                f"填寫乘客和會員資訊失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
    
    def _submit_booking(self, driver: webdriver.Edge, booking_id: int) -> None:
        """
        提交訂票
        
        Args:
            driver: WebDriver實例
            booking_id: 訂票ID（用於日誌）
        """
        try:
            # 點擊完成訂票按鈕
            submit_btn = driver.find_element(By.ID, "isSubmit")
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(1)
            
            # 處理二次確認視窗
            try:
                confirm_btn = driver.find_element(By.NAME, "SubmitButton")
                driver.execute_script("arguments[0].click();", confirm_btn)
                time.sleep(1)
            except NoSuchElementException:
                logger.debug(f"未找到確認按鈕 (booking_id: {booking_id})")
            
            # 關閉成功訊息
            try:
                close_btn = driver.find_element(By.CSS_SELECTOR, "input[value='關閉']")
                driver.execute_script("arguments[0].click();", close_btn)
                time.sleep(1)
            except NoSuchElementException:
                logger.debug(f"未找到關閉按鈕 (booking_id: {booking_id})")
        except Exception as e:
            logger.error(
                f"提交訂票失敗 (booking_id: {booking_id}): {str(e)}"
            )
            raise
