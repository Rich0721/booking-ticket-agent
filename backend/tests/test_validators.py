"""驗證工具測試 - 來源: Booking_Ticket.feature, Search_Ticket.feature"""
import unittest
from src.utils.validators import validate_tw_id, validate_date_format, validate_time_format

class TestValidators(unittest.TestCase):
    """驗證工具測試類別"""
    
    def test_validate_tw_id_valid(self):
        """測試有效的台灣身份證 - 來源: Booking_Ticket.feature/Search_Ticket.feature"""
        self.assertTrue(validate_tw_id('A123456789'))
    
    def test_validate_tw_id_invalid_format(self):
        """測試無效格式的台灣身份證 - 來源: Booking_Ticket.feature"""
        self.assertFalse(validate_tw_id('1234567890'))  # 不以字母開頭
        self.assertFalse(validate_tw_id('A12345678'))    # 長度不足
        self.assertFalse(validate_tw_id('A1234567890'))  # 長度過長
        self.assertFalse(validate_tw_id('a123456789'))   # 小寫字母
    
    def test_validate_tw_id_invalid_check_digit(self):
        """測試檢查碼不正確的台灣身份證 - 來源: Booking_Ticket.feature"""
        self.assertFalse(validate_tw_id('A123456788'))
    
    def test_validate_tw_id_invalid_second_digit(self):
        """測試第二位非1或2的台灣身份證 - 來源: Booking_Ticket.feature"""
        self.assertFalse(validate_tw_id('A023456789'))
        self.assertFalse(validate_tw_id('A323456789'))
    
    def test_validate_date_format_valid(self):
        """測試有效的日期格式 - 來源: Booking_Ticket.feature"""
        self.assertTrue(validate_date_format('2026-07-01'))
        self.assertTrue(validate_date_format('2026-07-03'))
        self.assertTrue(validate_date_format('2026-08-03'))
    
    def test_validate_date_format_invalid(self):
        """測試無效的日期格式 - 來源: Booking_Ticket.feature"""
        self.assertFalse(validate_date_format('2026/07/01'))
        self.assertFalse(validate_date_format('07-01-2026'))
        self.assertFalse(validate_date_format('2026-13-01'))  # 無效月份
    
    def test_validate_time_format_valid(self):
        """測試有效的時間格式 - 來源: Booking_Ticket.feature"""
        self.assertTrue(validate_time_format('10:30'))
        self.assertTrue(validate_time_format('22:00'))
        self.assertTrue(validate_time_format('00:00'))
    
    def test_validate_time_format_invalid(self):
        """測試無效的時間格式 - 來源: Booking_Ticket.feature"""
        self.assertFalse(validate_time_format('10:30:00'))
        self.assertFalse(validate_time_format('25:00'))  # 無效小時
        self.assertFalse(validate_time_format('10-30'))

if __name__ == '__main__':
    unittest.main()
