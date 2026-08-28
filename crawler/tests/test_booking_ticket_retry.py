"""
BookingTicketService重試機制測試
來源：Requirement - Driver卡住處理
- 場景1: 第一次訂票失敗加入重試列表
- 場景2: 重試成功則從失敗列表中移除
- 場景3: 重試失敗則標記為"Booking Error"
- 場景4: Driver超時時自動重啟並重試
"""

import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock, call
from src.services.BookingTicketService import BookingTicketService
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo


@pytest.fixture
def mock_repository():
    """Mock BookingTicketRepository"""
    with patch('src.services.BookingTicketService.BookingTicketRepository') as mock:
        yield mock.return_value


@pytest.fixture
def mock_web_driver_manager():
    """Mock CWebDriver"""
    with patch('src.services.BookingTicketService.CWebDriver.get_instance') as mock:
        yield mock.return_value


@pytest.fixture
def mock_two_captcha():
    """Mock TwoCaptcha"""
    with patch('src.services.BookingTicketService.TwoCaptcha') as mock:
        yield mock.return_value


@pytest.fixture
def booking_service(mock_repository, mock_web_driver_manager, mock_two_captcha):
    """創建BookingTicketService實例"""
    return BookingTicketService()


class TestBookingTicketServiceRetry:
    """BookingTicketService重試機制測試"""
    
    def test_failed_booking_added_to_retry_list(self, booking_service, mock_repository, mock_web_driver_manager):
        """
        場景1: 第一次訂票失敗加入重試列表
        如果卡住超過一定時間，則自動重啟Driver，並且該次操作資料加入Retry列表
        來源：Requirement - Driver卡住處理
        """
        # 設置模擬對象
        booking_info = CBookingTicketInfo(
            booking_id=1,
            user_id="A123456789",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="Normal",
            start_station="1",
            end_station="2",
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            is_early_bird=False,
            is_member=False,
            early_bird_ids=[]
        )
        
        mock_repository.get_booking_tickets_by_can_book_date.return_value = [booking_info]
        
        # 第一次訂票失敗
        with patch.object(booking_service, '_process_single_booking', return_value=False) as mock_process:
            successful, failed = booking_service.process_daily_bookings(date.today())
            
            # 檢查是否進行了重試
            assert mock_process.call_count >= 2  # 至少調用2次（初始 + 重試）
            
            # 檢查重試過程中的is_retry參數
            calls = mock_process.call_args_list
            first_call = calls[0]
            retry_call = calls[1]
            
            # 使用kwargs方式訪問參數
            first_kwargs = first_call.kwargs if hasattr(first_call, 'kwargs') else {}
            retry_kwargs = retry_call.kwargs if hasattr(retry_call, 'kwargs') else {}
            
            assert first_kwargs.get('is_retry', False) == False  # 第一次不是重試
            assert retry_kwargs.get('is_retry', False) == True   # 第二次是重試
    
    def test_successful_retry_removes_from_failed_list(self, booking_service, mock_repository, mock_web_driver_manager):
        """
        場景2: 重試成功則從失敗列表中移除
        來源：Requirement - Driver卡住處理
        """
        booking_info = CBookingTicketInfo(
            booking_id=1,
            user_id="A123456789",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="Normal",
            start_station="1",
            end_station="2",
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            is_early_bird=False,
            is_member=False,
            early_bird_ids=[]
        )
        
        mock_repository.get_booking_tickets_by_can_book_date.return_value = [booking_info]
        
        # 第一次失敗，第二次成功
        with patch.object(
            booking_service,
            '_process_single_booking',
            side_effect=[False, True]  # 第一次失敗，第二次成功
        ) as mock_process:
            successful, failed = booking_service.process_daily_bookings(date.today())
            
            # 檢查結果
            assert successful == 1  # 1個成功
            assert failed == 0      # 0個失敗
    
    def test_second_failure_marked_as_booking_error(self, booking_service, mock_repository, mock_web_driver_manager):
        """
        場景3: 如果已經在Retry階段，則自動重啟，但該次操作仍然視為失敗
        不再加入Retry列表，直接回填至Table為"Booking Error"
        來源：Requirement - Driver卡住處理
        """
        booking_info = CBookingTicketInfo(
            booking_id=1,
            user_id="A123456789",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="Normal",
            start_station="1",
            end_station="2",
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            is_early_bird=False,
            is_member=False,
            early_bird_ids=[]
        )
        
        mock_repository.get_booking_tickets_by_can_book_date.return_value = [booking_info]
        
        # 第一次失敗，第二次（重試）也失敗
        with patch.object(
            booking_service,
            '_process_single_booking',
            side_effect=[False, False]  # 兩次都失敗
        ):
            successful, failed = booking_service.process_daily_bookings(date.today())
            
            # 檢查結果
            assert successful == 0  # 0個成功
            assert failed == 1      # 1個失敗
            
            # 檢查是否標記為"Booking Error"
            mock_repository.update_ticket_number.assert_called_with(
                booking_info.booking_id,
                "Booking Error"
            )
    
    def test_multiple_bookings_with_mixed_results(self, booking_service, mock_repository, mock_web_driver_manager):
        """
        場景4: 多筆訂票，部分成功，部分失敗的情況
        來源：Requirement - Driver卡住處理
        """
        booking_info_1 = CBookingTicketInfo(
            booking_id=1,
            user_id="A123456789",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="Normal",
            start_station="1",
            end_station="2",
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            is_early_bird=False,
            is_member=False,
            early_bird_ids=[]
        )
        
        booking_info_2 = CBookingTicketInfo(
            booking_id=2,
            user_id="A123456788",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="Normal",
            start_station="1",
            end_station="2",
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            is_early_bird=False,
            is_member=False,
            early_bird_ids=[]
        )
        
        mock_repository.get_booking_tickets_by_can_book_date.return_value = [
            booking_info_1,
            booking_info_2
        ]
        
        # 第一筆成功，第二筆失敗後重試也失敗
        with patch.object(
            booking_service,
            '_process_single_booking',
            side_effect=[True, False, False]  # 第一筆成功，第二筆失敗，重試也失敗
        ):
            successful, failed = booking_service.process_daily_bookings(date.today())
            
            # 檢查結果
            assert successful == 1  # 1個成功
            assert failed == 1      # 1個失敗
    
    def test_retry_booking_id_tracking(self, booking_service, mock_repository, mock_web_driver_manager):
        """
        場景5: 追蹤已經重試過的booking IDs
        來源：Requirement - Driver卡住處理
        """
        booking_info = CBookingTicketInfo(
            booking_id=1,
            user_id="A123456789",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="Normal",
            start_station="1",
            end_station="2",
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            is_early_bird=False,
            is_member=False,
            early_bird_ids=[]
        )
        
        mock_repository.get_booking_tickets_by_can_book_date.return_value = [booking_info]
        
        # 第一次失敗，第二次（重試）成功
        with patch.object(
            booking_service,
            '_process_single_booking',
            side_effect=[False, True]
        ):
            booking_service.process_daily_bookings(date.today())
            
            # 檢查是否追蹤了重試的booking ID
            assert 1 in booking_service._BookingTicketService__retry_bookings
