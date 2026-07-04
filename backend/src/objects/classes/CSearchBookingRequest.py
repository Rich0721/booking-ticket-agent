from pydantic import BaseModel

from src.objects.classes.CBookingRequest import CRequestHeaders


class CSearchBookingInfo(BaseModel):
    user_id: str
    ticket_type: str


class CSearchBookingRequest(BaseModel):
    headers: CRequestHeaders
    info: CSearchBookingInfo
