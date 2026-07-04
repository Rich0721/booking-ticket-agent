from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from src.database.CBase import CBase


class CTableBookingTicket(CBase):
    __tablename__ = "TB_BOOKING_TICKET"

    booking_id: Mapped[int] = mapped_column("BOOKING_ID", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column("USER_ID", String(10), nullable=False)
    adult_count: Mapped[int] = mapped_column("ADULT_COUNT", Integer, default=0)
    child_count: Mapped[int] = mapped_column("CHILD_COUNT", Integer, default=0)
    student_count: Mapped[int] = mapped_column("STUDENT_COUNT", Integer, default=0)
    elder_count: Mapped[int] = mapped_column("ELDER_COUNT", Integer, default=0)
    disabled_count: Mapped[int] = mapped_column("DISABLED_COUNT", Integer, default=0)
    ticket_type: Mapped[str] = mapped_column("TICKET_TYPE", String(20), nullable=False)
    ticket_number: Mapped[str] = mapped_column("TICKET_NUMBER", String(20), default="")
    booking_date: Mapped[date] = mapped_column("BOOKING_DATE", Date, nullable=False)
    booking_time: Mapped[time] = mapped_column("BOOKING_TIME", Time, nullable=False)
    start_station: Mapped[str] = mapped_column("START_STATION", String(50), nullable=False)
    end_station: Mapped[str] = mapped_column("END_STATION", String(50), nullable=False)
    is_early_bird: Mapped[bool] = mapped_column("IS_EARLY_BIRD", Boolean, default=False)
    is_member: Mapped[bool] = mapped_column("IS_MEMBER", Boolean, default=False)
    can_book_date: Mapped[date] = mapped_column("CAN_BOOK_DATE", Date, nullable=False)
    created_time: Mapped[datetime] = mapped_column("CREATED_TIME", DateTime, default=datetime.utcnow)
    updated_time: Mapped[datetime] = mapped_column(
        "UPDATED_TIME", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
