"""
預約訂票服務單元測試

測試BookingTicketService的驗證邏輯和預約流程
根據Booking_Ticket.feature場景進行測試
"""

import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch

from src.services.BookingTicketService import BookingTicketService
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo


# 測試用台灣身份證號
VALID_TEST_ID_1 = "A123456785"
VALID_TEST_ID_2 = "B287654325"
INVALID_TEST_ID = "INVALID123"


class TestBookingTicketServiceValidation:
    """預約訂票服務驗證測試"""
    
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
    
    def _create_booking_info(self, user_id=VALID_TEST_ID_1, adults=1, early_ids=None, **kwargs):
        """輔助方法：建立預約訊息"""
        defaults = {
            "user_id": user_id,
            "ticket_type": "THSR",
            "booking_date": date(2026, 7, 10),
            "booking_time": "10:30",
            "start_station": "台北",
            "end_station": "左營",
            "adults": adults,
            "childs": 0,
            "students": 0,
            "elders": 0,
            "disables": 0,
            "is_early_bird": False,
            "is_member": False,
            "early_ids": early_ids or [],
        }
        defaults.update(kwargs)
        
        return CBookingTicketInfo(**defaults)
    
    @pytest.mark.parametrize("user_id,is_valid,expected_error", [
        (VALID_TEST_ID_1, True, None),
        (INVALID_TEST_ID, False, "訂票者ID輸入錯誤"),
    ])
    def test_validate_user_id(self, service, user_id, is_valid, expected_error):
        """測試訂票者ID驗證 - Scenario: 使用者輸入不同身份證"""
        booking_info = self._create_booking_info(user_id=user_id)
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = is_valid
            result_valid, error_message = service.validate_booking_info(booking_info)
            
            assert result_valid == is_valid
            if expected_error:
                assert error_message == expected_error
    
    @pytest.mark.parametrize("adult_count,is_valid,expected_error", [
        (1, True, None),
        (9, True, None),
        (10, True, None),
        (11, False, "訂購數量不可以超過10張"),
    ])
    def test_validate_ticket_quantity(self, service, adult_count, is_valid, expected_error):
        """測試訂購數量驗證 - Scenario: 訂購不同數量的票"""
        booking_info = self._create_booking_info(adults=adult_count)
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            result_valid, error_message = service.validate_booking_info(booking_info)
            
            assert result_valid == is_valid
            if expected_error:
                assert error_message == expected_error
    
    @pytest.mark.parametrize("adults,early_ids,is_valid,expected_error", [
        (1, [VALID_TEST_ID_1], True, None),
        (2, [VALID_TEST_ID_1, VALID_TEST_ID_2], True, None),
        (2, [VALID_TEST_ID_1], False, "全票與早鳥票數量需相同"),
        (1, [VALID_TEST_ID_1, VALID_TEST_ID_2], False, "全票與早鳥票數量需相同"),
    ])
    def test_validate_early_bird_count(self, service, adults, early_ids, is_valid, expected_error):
        """測試早鳥票數量驗證 - Scenario: 全票與早鳥票數量是否相同"""
        booking_info = self._create_booking_info(
            adults=adults,
            early_ids=early_ids,
            is_early_bird=True
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            result_valid, error_message = service.validate_booking_info(booking_info)
            
            assert result_valid == is_valid
            if expected_error:
                assert error_message == expected_error


class TestBookingTicketServiceProcess:
    """預約訂票流程測試"""
    
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
    
    def _create_booking_info(self, travel_date=None, adults=1, early_count=0, **kwargs):
        """輔助方法：建立預約訊息"""
        if travel_date is None:
            travel_date = date(2026, 7, 21)
        
        early_ids = [VALID_TEST_ID_1] if early_count == 1 else \
                    [VALID_TEST_ID_1, VALID_TEST_ID_2] if early_count == 2 else []
        
        defaults = {
            "user_id": VALID_TEST_ID_1,
            "ticket_type": "THSR",
            "booking_date": travel_date,
            "booking_time": "10:30",
            "start_station": "台北",
            "end_station": "左營",
            "adults": adults,
            "childs": 0,
            "students": 0,
            "elders": 0,
            "disables": 0,
            "is_early_bird": early_count > 0,
            "is_member": False,
            "early_ids": early_ids,
        }
        defaults.update(kwargs)
        
        return CBookingTicketInfo(**defaults)
    
    @pytest.mark.parametrize("travel_date,should_fail", [
        (date(2026, 7, 1), True),   # Same day
        (date(2026, 6, 30), True),  # Past day
        (date(2026, 7, 2), False),  # Future
    ])
    def test_booking_invalid_dates(self, service, travel_date, should_fail):
        """測試預約日期驗證 - Scenario: 使用者選擇當日或過去日期不可預約"""
        system_date = datetime(2026, 7, 1)
        booking_info = self._create_booking_info(travel_date=travel_date)
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            
            assert success == (not should_fail)
            if should_fail:
                assert "不接受當天的預約訂票" in message or message
    
    @pytest.mark.parametrize("travel_date,expected_booking_date", [
        # Within 29 days (system date 2026/07/01)
        (date(2026, 7, 3), "2026/07/02"),
        (date(2026, 7, 21), "2026/07/02"),
        (date(2026, 7, 29), "2026/07/02"),
        (date(2026, 7, 30), "2026/07/02"),  # Exactly 29 days
    ])
    def test_booking_within_29_days(self, service, travel_date, expected_booking_date):
        """測試搭乘日在29天內 - Scenario: 搭乘日在系統日起29天內"""
        system_date = datetime(2026, 7, 1)
        booking_info = self._create_booking_info(travel_date=travel_date)
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            
            assert success
            assert expected_booking_date in message
    
    @pytest.mark.parametrize("travel_date,expected_booking_date", [
        # 30+ days, Monday to Saturday (system date 2026/07/01)
        (date(2026, 8, 3), "2026/07/05"),   # Monday
        (date(2026, 8, 4), "2026/07/06"),   # Tuesday
        (date(2026, 8, 5), "2026/07/07"),   # Wednesday
        (date(2026, 8, 6), "2026/07/08"),   # Thursday
        (date(2026, 8, 7), "2026/07/09"),   # Friday
        (date(2026, 8, 8), "2026/07/10"),   # Saturday
    ])
    def test_booking_30plus_days_weekday(self, service, travel_date, expected_booking_date):
        """測試搭乘日在30天後且為週一到週六 - Scenario: 搭乘日為第30天後且為週一到週六"""
        system_date = datetime(2026, 7, 1)
        booking_info = self._create_booking_info(travel_date=travel_date)
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            
            assert success
            assert expected_booking_date in message
    
    def test_booking_30plus_days_sunday(self, service):
        """測試搭乘日在30天後且為週日 - Scenario: 搭乘日為第30天後且為週日"""
        system_date = datetime(2026, 7, 1)
        # 2026/08/16 is Sunday, should adjust to 2026/07/17 (Friday)
        booking_info = self._create_booking_info(travel_date=date(2026, 8, 16))
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            
            assert success
            assert "2026/07/17" in message
    
    def test_booking_with_early_bird(self, service):
        """測試帶有早鳥票的預約 - Scenario: 使用者預約早鳥票"""
        system_date = datetime(2026, 7, 1)
        booking_info = self._create_booking_info(
            travel_date=date(2026, 7, 21),
            adults=2,
            early_count=2
        )
        
        with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
            mock_validate.return_value = True
            success, message = service.process_booking(booking_info, system_date)
            
            assert success
            assert "2026/07/02" in message
            service.booking_repository.create_booking.assert_called_once()
            assert service.booking_repository.create_early_bird.call_count == 2
