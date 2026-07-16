from datetime import datetime, date
from typing import Optional
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo
from src.utils.id_validator import validate_taiwan_id
from src.utils.date_calculator import calculate_booking_date


class BookingTicketService:
    """預約訂票服務"""
    
    def __init__(self, booking_repository):
        self.booking_repository = booking_repository
    
    def validate_booking_info(self, booking_info: CBookingTicketInfo) -> tuple[bool, str]:
        """
        驗證預約訂票資訊
        
        Args:
            booking_info: 預約訂票資訊
            
        Returns:
            (is_valid, error_message)
        """
        # 驗證訂票者ID
        if not validate_taiwan_id(booking_info.user_id):
            return False, "訂票者ID輸入錯誤"
        
        # 驗證訂購數量
        total_count = booking_info.get_total_count()
        if total_count > 10:
            return False, "訂購數量不可以超過10張"
        
        # 驗證早鳥票
        if booking_info.is_early_bird:
            if len(booking_info.early_ids) != booking_info.adults:
                return False, "全票與早鳥票數量需相同"
            
            # 驗證所有早鳥票ID
            for early_id in booking_info.early_ids:
                if not validate_taiwan_id(early_id):
                    return False, "訂票者ID輸入錯誤"
        
        return True, ""
    
    def process_booking(
        self,
        booking_info: CBookingTicketInfo,
        system_date: datetime
    ) -> tuple[bool, str]:
        """
        處理預約訂票
        
        Args:
            booking_info: 預約訂票資訊
            system_date: 系統日期
            
        Returns:
            (success, message)
        """
        # 驗證預約訂票資訊
        is_valid, error_message = self.validate_booking_info(booking_info)
        if not is_valid:
            return False, error_message
        
        # 轉換booking_date為datetime
        travel_datetime = datetime.combine(booking_info.booking_date, datetime.strptime(booking_info.booking_time, "%H:%M").time())
        travel_date = booking_info.booking_date
        system_date_only = system_date.date() if isinstance(system_date, datetime) else system_date
        
        # 計算可訂購日期
        try:
            can_book_date = calculate_booking_date(system_date_only, travel_date)
        except ValueError as e:
            return False, str(e)
        
        # 新增至資料庫
        booking_id = self.booking_repository.create_booking(
            user_id=booking_info.user_id,
            ticket_type=booking_info.ticket_type,
            adult_count=booking_info.adults,
            child_count=booking_info.childs,
            student_count=booking_info.students,
            elder_count=booking_info.elders,
            disabled_count=booking_info.disables,
            booking_date=booking_info.booking_date,
            booking_time=booking_info.booking_time,
            start_station=booking_info.start_station,
            end_station=booking_info.end_station,
            is_early_bird=booking_info.is_early_bird,
            is_member=booking_info.is_member,
            can_book_date=can_book_date
        )
        
        # 如果有早鳥票，新增早鳥票使用者
        if booking_info.is_early_bird:
            for early_id in booking_info.early_ids:
                self.booking_repository.create_early_bird(
                    booking_id=booking_id,
                    user_id=early_id
                )
        
        # 生成回傳訊息
        message = f"{can_book_date.strftime('%Y/%m/%d')}將完成訂票，請記得查詢取票號碼"
        
        return True, message
