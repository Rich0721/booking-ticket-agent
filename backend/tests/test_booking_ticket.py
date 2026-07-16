import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch
from src.services.BookingTicketService import BookingTicketService
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo
from src.utils.date_calculator import calculate_booking_date


# 有效的測試用台灣身份證號 (測試用ID)
VALID_TEST_ID_1 = "A123456785"
VALID_TEST_ID_2 = "B287654325"
INVALID_TEST_ID = "INVALID123"


class TestBookingTicketService:
    """預約訂票服務測試"""
    
    @pytest.fixture
    def mock_repository(self):
        """建立mock repository"""
        mock = Mock()
        mock.create_booking.return_value = 1
        mock.create_early_bird.return_value = 1
        return mock
    
    @pytest.fixture
    def service(self, mock_repository):
        """建立服務實例"""
        return BookingTicketService(mock_repository)
    
    def test_validate_invalid_user_id(self, service):
        """測試無效的訂票者ID - Scenario: 使用者輸入錯誤的身份證編號"""
        booking_info = CBookingTicketInfo(
            user_id=INVALID_TEST_ID,
            ticket_type="THSR",
            booking_date=date(2026, 7, 10),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=1,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = False
            is_valid, error_message = service.validate_booking_info(booking_info)
            assert not is_valid
            assert error_message == "訂票者ID輸入錯誤"
    
    def test_validate_exceeds_ticket_limit(self, service):
        """測試超過訂購數量限制 - Scenario: 訂購超過10張票"""
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 7, 10),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=11,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            is_valid, error_message = service.validate_booking_info(booking_info)
            assert not is_valid
            assert error_message == "訂購數量不可以超過10張"
    
    def test_validate_mismatched_early_bird_count(self, service):
        """測試早鳥票數量不符 - Scenario: 全票與早鳥票數量不相同"""
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 7, 10),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=2,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=True,
            is_member=False,
            early_ids=[VALID_TEST_ID_1]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            is_valid, error_message = service.validate_booking_info(booking_info)
            assert not is_valid
            assert error_message == "全票與早鳥票數量需相同"
    
    def test_booking_same_day_rejection(self, service):
        """測試當日不可預約 - Scenario: 使用者選擇當日日期"""
        system_date = datetime(2026, 7, 1)
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 7, 1),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=1,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            assert not success
            assert "不接受當天的預約訂票" in message
    
    def test_booking_past_day_rejection(self, service):
        """測試過去日期不可預約 - Scenario: 使用者選擇過去日期"""
        system_date = datetime(2026, 7, 1)
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 6, 30),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=1,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            assert not success
    
    def test_booking_within_29_days(self, service):
        """測試搭乘日在29天內 - Scenario: 系統日為2026/07/01, 搭乘日2026/07/21"""
        system_date = datetime(2026, 7, 1)
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 7, 21),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=1,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            assert success
            assert "2026/07/02" in message
    
    def test_booking_30plus_days_monday(self, service):
        """測試搭乘日在30天後且為週一 - Scenario: 系統日2026/07/01, 搭乘日2026/08/03(一)"""
        system_date = datetime(2026, 7, 1)
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 8, 3),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=1,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            assert success
            assert "2026/07/05" in message
    
    def test_booking_30plus_days_sunday(self, service):
        """測試搭乘日在30天後且為週日 - Scenario: 系統日2026/07/01, 搭乘日2026/08/02(日)"""
        system_date = datetime(2026, 7, 1)
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 8, 2),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=1,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=False,
            is_member=False,
            early_ids=[]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            assert success
            assert "2026/07/03" in message
    
    def test_booking_with_early_bird(self, service):
        """測試帶有早鳥票的預約 - Scenario: 使用者預約早鳥票"""
        system_date = datetime(2026, 7, 1)
        booking_info = CBookingTicketInfo(
            user_id=VALID_TEST_ID_1,
            ticket_type="THSR",
            booking_date=date(2026, 7, 21),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            adults=2,
            childs=0,
            students=0,
            elders=0,
            disables=0,
            is_early_bird=True,
            is_member=False,
            early_ids=[VALID_TEST_ID_1, VALID_TEST_ID_2]
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            assert success
            assert "2026/07/02" in message
            service.booking_repository.create_booking.assert_called_once()
            assert service.booking_repository.create_early_bird.call_count == 2


class TestDateCalculator:
    """日期計算器測試"""
    
    def test_date_within_29_days(self):
        """測試29天內的日期計算 - Scenario: 搭乘日在29天內"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 7, 21)
        result = calculate_booking_date(system_date, travel_date)
        assert result == date(2026, 7, 2)
    
    def test_date_exactly_29_days(self):
        """測試恰好29天的日期計算"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 7, 30)
        result = calculate_booking_date(system_date, travel_date)
        assert result == date(2026, 7, 2)
    
    def test_date_30plus_days_monday(self):
        """測試30天後週一的日期計算 - Scenario: 搭乘日2026/08/03(一)"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 8, 3)
        result = calculate_booking_date(system_date, travel_date)
        assert result == date(2026, 7, 5)
    
    def test_date_30plus_days_sunday(self):
        """測試30天後週日的日期計算 - Scenario: 搭乘日為週日調整至週五"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 8, 2)
        result = calculate_booking_date(system_date, travel_date)
        assert result == date(2026, 7, 3)
        assert result.weekday() == 4  # Friday
    
    def test_date_same_day_error(self):
        """測試當日會拋出錯誤"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 7, 1)
        with pytest.raises(ValueError, match="不接受當天的預約訂票"):
            calculate_booking_date(system_date, travel_date)
    
    def test_date_past_day_error(self):
        """測試過去日期會拋出錯誤"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 6, 30)
        with pytest.raises(ValueError, match="不接受當天的預約訂票"):
            calculate_booking_date(system_date, travel_date)
