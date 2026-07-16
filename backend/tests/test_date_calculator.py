"""
日期計算器單元測試

測試calculate_booking_date函數的各種場景
根據Booking_Ticket.feature場景進行測試
"""

import pytest
from datetime import date

from src.utils.date_calculator import calculate_booking_date


class TestDateCalculator:
    """日期計算器測試"""
    
    @pytest.mark.parametrize("system_date,travel_date,expected_date", [
        # Within 29 days: system_date + 1
        (date(2026, 7, 1), date(2026, 7, 3), date(2026, 7, 2)),
        (date(2026, 7, 1), date(2026, 7, 21), date(2026, 7, 2)),
        (date(2026, 7, 1), date(2026, 7, 29), date(2026, 7, 2)),
        (date(2026, 7, 1), date(2026, 7, 30), date(2026, 7, 2)),  # Exactly 29 days
    ])
    def test_booking_within_29_days(self, system_date, travel_date, expected_date):
        """測試搭乘日在29天內 - Scenario: 搭乘日在系統日起29天內"""
        result = calculate_booking_date(system_date, travel_date)
        assert result == expected_date
    
    @pytest.mark.parametrize("travel_date,expected_date,weekday_name", [
        # 30+ days, Monday to Saturday: travel_date - 29 days
        (date(2026, 8, 3), date(2026, 7, 5), "Sunday"),
        (date(2026, 8, 4), date(2026, 7, 6), "Monday"),
        (date(2026, 8, 5), date(2026, 7, 7), "Tuesday"),
        (date(2026, 8, 6), date(2026, 7, 8), "Wednesday"),
        (date(2026, 8, 7), date(2026, 7, 9), "Thursday"),
        (date(2026, 8, 8), date(2026, 7, 10), "Friday"),
    ])
    def test_booking_30plus_days_weekday(self, travel_date, expected_date, weekday_name):
        """測試搭乘日在30天後且為週一到週六 - Scenario: 搭乘日為第30天後且為週一到週六"""
        system_date = date(2026, 7, 1)
        result = calculate_booking_date(system_date, travel_date)
        assert result == expected_date
    
    def test_booking_30plus_days_sunday(self):
        """測試搭乘日在30天後且為週日 - Scenario: 搭乘日為第30天後且為週日"""
        system_date = date(2026, 7, 1)
        travel_date = date(2026, 8, 16)  # Sunday
        
        result = calculate_booking_date(system_date, travel_date)
        
        # Should adjust to nearest Friday (2026/07/17)
        assert result == date(2026, 7, 17)
        assert result.weekday() == 4  # Friday
    
    @pytest.mark.parametrize("travel_date,error_message", [
        (date(2026, 7, 1), "不接受當天的預約訂票"),  # Same day
        (date(2026, 6, 30), "不接受當天的預約訂票"),  # Past day
    ])
    def test_booking_invalid_dates(self, travel_date, error_message):
        """測試無效日期 - Scenario: 搭乘日為當日或過去不可預約"""
        system_date = date(2026, 7, 1)
        
        with pytest.raises(ValueError, match=error_message):
            calculate_booking_date(system_date, travel_date)
