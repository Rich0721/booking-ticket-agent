from pydantic import BaseModel

from src.objects.classes.CBookingRequest import CRequestHeaders


class CDeleteBookingInfo(BaseModel):
    booking_id: int
    user_id: str
    ticket_type: str


class CDeleteBookingRequest(BaseModel):
    headers: CRequestHeaders
    info: CDeleteBookingInfo
