"""
預約訂票ORM模型定義
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, DateTime, ForeignKey, BIGINT
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BookingTicket(Base):
    """預約訂票表模型"""
    __tablename__ = "TB_BOOKING_THICKET"
    
    booking_id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(String(10), nullable=False)
    adult_count = Column(Integer)
    child_count = Column(Integer)
    student_count = Column(Integer)
    elder_count = Column(Integer)
    disabled_count = Column(Integer)
    ticket_type = Column(String(20), nullable=False)
    ticket_number = Column(String(20), nullable=False)
    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time, nullable=False)
    start_station = Column(String(50), nullable=False)
    end_station = Column(String(50), nullable=False)
    is_early_bird = Column(Boolean, default=False)
    is_member = Column(Boolean, default=False)
    can_book_date = Column(Date, nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    early_birds = relationship("EarlyBird", back_populates="booking")


class EarlyBird(Base):
    """早鳥票表模型"""
    __tablename__ = "TB_EARLY_BIRD"
    
    early_bird_id = Column(BIGINT, primary_key=True, autoincrement=True)
    booking_id = Column(BIGINT, ForeignKey("TB_BOOKING_THICKET.booking_id"), nullable=False)
    user_id = Column(String(10), nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    booking = relationship("BookingTicket", back_populates="early_birds")
