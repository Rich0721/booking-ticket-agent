from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.CBase import CBase


class CTableEarlyBird(CBase):
    __tablename__ = "TB_EARLY_BIRD"

    early_bird_id: Mapped[int] = mapped_column("EARLY_BIRD_ID", Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(
        "BOOKING_ID", Integer, ForeignKey("TB_BOOKING_TICKET.BOOKING_ID"), nullable=False
    )
    user_id: Mapped[str] = mapped_column("USER_ID", String(10), nullable=False)
    created_time: Mapped[datetime] = mapped_column("CREATED_TIME", DateTime, default=datetime.utcnow)
    updated_time: Mapped[datetime] = mapped_column(
        "UPDATED_TIME", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
