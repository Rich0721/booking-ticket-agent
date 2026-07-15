"""驗證相關工具函式"""
import re
from datetime import datetime

def validate_tw_id(user_id: str) -> bool:
    """
    驗證台灣身份證編碼
    
    根據台灣身份證編碼規則進行驗證：
    - 第一碼為大寫字母
    - 第二碼為1或2
    - 後8碼為數字
    - 最後一碼為檢查碼
    
    Args:
        user_id: 身份證字號
        
    Returns:
        bool: 是否為有效的身份證
    """
    if not isinstance(user_id, str) or len(user_id) != 10:
        return False
    
    # 基本格式檢查
    if not re.match(r'^[A-Z][12]\d{8}$', user_id):
        return False
    
    # 字母轉換表
    letter_map = {
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17,
        'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'O': 35, 'P': 23,
        'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29, 'W': 32, 'X': 30,
        'Y': 31, 'Z': 33
    }
    
    # 計算檢查碼
    checksum = 0
    
    # 第一碼（字母）
    first_code = letter_map.get(user_id[0], 0)
    checksum += (first_code // 10) + (first_code % 10) * 9
    
    # 第二碼到第九碼
    for i in range(1, 9):
        checksum += int(user_id[i]) * (9 - i)
    
    # 計算應得的檢查碼
    check_digit = (10 - (checksum % 10)) % 10
    
    return check_digit == int(user_id[9])


def validate_date_format(date_str: str) -> bool:
    """
    驗證日期格式 (YYYY-MM-DD)
    
    Args:
        date_str: 日期字符串
        
    Returns:
        bool: 是否為有效日期格式
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_time_format(time_str: str) -> bool:
    """
    驗證時間格式 (HH:MM)
    
    Args:
        time_str: 時間字符串
        
    Returns:
        bool: 是否為有效時間格式
    """
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False
