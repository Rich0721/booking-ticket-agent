from datetime import date, time

from pydantic import BaseModel, Field


class CRequestHeaders(BaseModel):
    status_code: int | None = None
    user_agent: str = Field(min_length=1)


class CBookingInfo(BaseModel):
    user_id: str
    ticket_type: str
    booking_date: date
    booking_time: time
    start_station: str
    end_station: str
    adults: int = 0
    childs: int = 0
    students: int = 0
    elders: int = 0
    disables: int = 0
    is_early_bird: bool = False
    is_member: bool = False
    early_ids: list[str] = Field(default_factory=list)


class CBookingRequest(BaseModel):
    headers: CRequestHeaders
    info: CBookingInfo
