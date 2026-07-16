from datetime import datetime, date
from typing import List


class CBookingTicketInfo:
    """預約訂票資訊類別"""
    
    def __init__(
        self,
        user_id: str,
        ticket_type: str,
        booking_date: date,
        booking_time: str,
        start_station: str,
        end_station: str,
        adults: int,
        childs: int,
        students: int,
        elders: int,
        disables: int,
        is_early_bird: bool,
        is_member: bool,
        early_ids: List[str]
    ):
        self.user_id = user_id
        self.ticket_type = ticket_type
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.start_station = start_station
        self.end_station = end_station
        self.adults = adults
        self.childs = childs
        self.students = students
        self.elders = elders
        self.disables = disables
        self.is_early_bird = is_early_bird
        self.is_member = is_member
        self.early_ids = early_ids
    
    def get_total_count(self) -> int:
        """取得總購票數量"""
        return self.adults + self.childs + self.students + self.elders + self.disables
