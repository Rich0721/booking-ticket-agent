from datetime import date, time
from typing import List, Optional


class CBookingTicketInfo:
    """訂票資訊類"""
    
    def __init__(
        self,
        booking_id: int,
        user_id: str,
        adult_count: int,
        child_count: int,
        student_count: int,
        elder_count: int,
        disabled_count: int,
        ticket_type: str,
        booking_date: date,
        booking_time: time,
        start_station: str,
        end_station: str,
        is_early_bird: bool = False,
        is_member: bool = False,
        can_book_date: date = None,
        ticket_number: Optional[str] = None,
        early_bird_ids: List[int] = None
    ):
        self.booking_id = booking_id
        self.user_id = user_id
        self.adult_count = adult_count
        self.child_count = child_count
        self.student_count = student_count
        self.elder_count = elder_count
        self.disabled_count = disabled_count
        self.ticket_type = ticket_type
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.start_station = start_station
        self.end_station = end_station
        self.is_early_bird = is_early_bird
        self.is_member = is_member
        self.can_book_date = can_book_date
        self.ticket_number = ticket_number
        self.early_bird_ids = early_bird_ids or []
