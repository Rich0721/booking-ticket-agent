"""日期相關工具函式"""
from datetime import datetime, timedelta

def calculate_booking_completion_date(system_date: datetime, departure_date: datetime) -> datetime:
    """
    計算訂票完成日期
    
    規則：
    1. 不接受當天的預約訂票
    2. 預約日期在29天內：系統日+1就可以開放使用者查詢
    3. 預約日期在29天以後且為週一到週六：用搭乘時間往前算29天為完成訂票日期
    4. 預約日期在29天以後且為週日：可提早至離29日最近的週五
    
    Args:
        system_date: 系統日期
        departure_date: 搭乘日期
        
    Returns:
        datetime: 訂票完成日期
        
    Raises:
        ValueError: 搭乘日期不符合條件
    """
    # 檢查是否為當天或過去日期
    if departure_date.date() <= system_date.date():
        raise ValueError("當天不接受預約訂票")
    
    # 計算差天數
    days_diff = (departure_date.date() - system_date.date()).days
    
    if days_diff <= 29:
        # 29天內：系統日+1
        return system_date + timedelta(days=1)
    else:
        # 29天以後
        # 往前算29天
        completion_date = departure_date - timedelta(days=29)
        
        # 檢查搭乘日期是否為週日 (weekday() == 6 表示週日)
        if departure_date.weekday() == 6:
            # 搭乘日為週日：從往前算29天的結果往前推至最近的週五
            while completion_date.weekday() != 4:  # 4 = 週五
                completion_date -= timedelta(days=1)
        
        return completion_date


def get_message_for_booking_date(completion_date: datetime) -> str:
    """
    根據訂票完成日期生成對應的訊息
    
    Args:
        completion_date: 訂票完成日期
        
    Returns:
        str: 訊息內容
    """
    date_str = completion_date.strftime('%Y/%m/%d')
    return f"{date_str}將完成訂票，請記得查詢取票號碼"


def parse_date_string(date_str: str) -> datetime:
    """
    解析日期字符串 (YYYY-MM-DD)
    
    Args:
        date_str: 日期字符串
        
    Returns:
        datetime: 解析後的日期對象
    """
    return datetime.strptime(date_str, '%Y-%m-%d')
