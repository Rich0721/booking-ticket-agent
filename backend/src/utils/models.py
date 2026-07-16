from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class BookingTicketRequest(BaseModel):
    user_id: str
    ticket_type: str
    booking_date: str
    booking_time: str
    start_station: str
    end_station: str
    adults: int
    childs: int
    students: int
    elders: int
    disables: int
    is_early_bird: bool
    is_member: bool
    early_ids: List[str]


class BookingTicketResponse(BaseModel):
    message: str
