from datetime import datetime, timedelta


def calculate_booking_date(system_date: datetime, travel_date: datetime) -> datetime:
    """
    根據旅行日期計算可訂購日期
    
    Rules:
    1. 不接受當天的預約訂票
    2. 如果在29天內，系統日+1可開放查詢
    3. 如果在29天以後且為週一到週六，往前算29天
    4. 如果在29天以後且為週日，往前至離29日最近的週五
    
    Args:
        system_date: 系統日期
        travel_date: 旅行日期
        
    Returns:
        可訂購日期
        
    Raises:
        ValueError: 如果旅行日期不符合規則
    """
    days_diff = (travel_date - system_date).days
    
    # 檢查不能預約當日或過去
    if days_diff <= 0:
        raise ValueError("不接受當天的預約訂票")
    
    # 29天以內，系統日+1
    if days_diff <= 29:
        return system_date + timedelta(days=1)
    
    # 29天以後
    # 計算往前29天的日期
    booking_date = travel_date - timedelta(days=29)
    
    # 如果旅行日期為週日(weekday() = 6)，需要調整訂票日期到最近的週五
    if travel_date.weekday() == 6:  # 旅行日期是週日
        # 計算出的訂票日期往前調整到最近的週五
        # weekday(): 0=一, 1=二, 2=三, 3=四, 4=五, 5=六, 6=日
        days_from_friday = (booking_date.weekday() - 4) % 7
        if days_from_friday > 0:
            booking_date = booking_date - timedelta(days=days_from_friday)
    
    return booking_date
