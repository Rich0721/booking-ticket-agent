"""日期計算工具測試 - 來源: Booking_Ticket.feature"""
import unittest
from datetime import datetime
from src.utils.date_helper import calculate_booking_completion_date, get_message_for_booking_date, parse_date_string

class TestDateHelper(unittest.TestCase):
    """日期計算工具測試類別"""
    
    def setUp(self):
        """設置系統日期為 2026/07/01"""
        self.system_date = datetime(2026, 7, 1)
    
    def test_calculate_same_day_should_fail(self):
        """測試當天日期應拋出錯誤 - 來源: Booking_Ticket.feature Rule: 搭乘日為當日或過去不可預約"""
        departure_date = datetime(2026, 7, 1)
        with self.assertRaises(ValueError) as context:
            calculate_booking_completion_date(self.system_date, departure_date)
        self.assertIn('當天不接受預約訂票', str(context.exception))
    
    def test_calculate_past_day_should_fail(self):
        """測試過去日期應拋出錯誤 - 來源: Booking_Ticket.feature Rule: 搭乘日為當日或過去不可預約"""
        departure_date = datetime(2026, 6, 30)
        with self.assertRaises(ValueError) as context:
            calculate_booking_completion_date(self.system_date, departure_date)
        self.assertIn('當天不接受預約訂票', str(context.exception))
    
    def test_calculate_within_29_days(self):
        """
        測試搭乘日在29天內，應為系統日+1
        
        來源: Booking_Ticket.feature Rule: 搭乘日在系統日起29天內
        - 系統日為 2026/07/01
        - 搭乘日 2026/07/03 -> 預期 2026/07/02
        - 搭乘日 2026/07/21 -> 預期 2026/07/02
        - 搭乘日 2026/07/29 -> 預期 2026/07/02
        """
        test_cases = [
            (datetime(2026, 7, 3), datetime(2026, 7, 2)),
            (datetime(2026, 7, 21), datetime(2026, 7, 2)),
            (datetime(2026, 7, 29), datetime(2026, 7, 2)),
        ]
        
        for departure_date, expected_completion in test_cases:
            result = calculate_booking_completion_date(self.system_date, departure_date)
            self.assertEqual(result.date(), expected_completion.date(), 
                           f"搭乘日 {departure_date.date()} 計算結果應為 {expected_completion.date()}")
    
    def test_calculate_after_29_days_weekday(self):
        """
        測試搭乘日在29天後且為週一到週六，應往前算29天
        
        來源: Booking_Ticket.feature Rule: 搭乘日為第30天後且搭為週一到週六
        - 系統日為 2026/07/01
        - 搭乘日 2026/08/03(一) -> 預期 2026/07/05
        - 搭乘日 2026/08/04(二) -> 預期 2026/07/06
        - 搭乘日 2026/08/05(三) -> 預期 2026/07/07
        - 搭乘日 2026/08/06(四) -> 預期 2026/07/08
        - 搭乘日 2026/08/07(五) -> 預期 2026/07/09
        - 搭乘日 2026/08/08(六) -> 預期 2026/07/10
        """
        test_cases = [
            (datetime(2026, 8, 3), datetime(2026, 7, 5)),   # 一
            (datetime(2026, 8, 4), datetime(2026, 7, 6)),   # 二
            (datetime(2026, 8, 5), datetime(2026, 7, 7)),   # 三
            (datetime(2026, 8, 6), datetime(2026, 7, 8)),   # 四
            (datetime(2026, 8, 7), datetime(2026, 7, 9)),   # 五
            (datetime(2026, 8, 8), datetime(2026, 7, 10)),  # 六
        ]
        
        for departure_date, expected_completion in test_cases:
            result = calculate_booking_completion_date(self.system_date, departure_date)
            self.assertEqual(result.date(), expected_completion.date(),
                           f"搭乘日 {departure_date.date()} ({departure_date.strftime('%A')}) 計算結果應為 {expected_completion.date()}")
    
    def test_calculate_after_29_days_sunday(self):
        """
        測試搭乘日在29天後且為週日，應往前推至最近的週五
        
        來源: Booking_Ticket.feature Example:搭乘日為第30天後且為週日
        - 系統日為 2026/07/01
        - 搭乘日 2026/08/16(日) -> 預期 2026/07/17(五)
        """
        departure_date = datetime(2026, 8, 16)  # 週日
        expected_completion = datetime(2026, 7, 17)  # 週五
        
        result = calculate_booking_completion_date(self.system_date, departure_date)
        self.assertEqual(result.date(), expected_completion.date(),
                       f"搭乘日 {departure_date.date()} (週日) 計算結果應為 {expected_completion.date()} (週五)")
    
    def test_get_message_for_booking_date(self):
        """測試訊息生成 - 來源: Booking_Ticket.feature"""
        completion_date = datetime(2026, 7, 2)
        message = get_message_for_booking_date(completion_date)
        self.assertIn('2026/07/02', message)
        self.assertIn('將完成訂票', message)
    
    def test_parse_date_string(self):
        """測試日期字符串解析 - 來源: Booking_Ticket.feature"""
        date_str = '2026-07-03'
        result = parse_date_string(date_str)
        self.assertEqual(result.year, 2026)
        self.assertEqual(result.month, 7)
        self.assertEqual(result.day, 3)

if __name__ == '__main__':
    unittest.main()
