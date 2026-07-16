from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.objects.models.booking_ticket_models import BookingTicket, EarlyBird


class BookingTicketRepository:
    """預約訂票資料庫操作"""
    
    def __init__(self, db_session: Session):
        """
        初始化Repository
        
        Args:
            db_session: SQLAlchemy Session對象
        """
        self.db = db_session
    
    def create_booking(
        self,
        user_id: str,
        ticket_type: str,
        adult_count: int,
        child_count: int,
        student_count: int,
        elder_count: int,
        disabled_count: int,
        booking_date: date,
        booking_time: str,
        start_station: str,
        end_station: str,
        is_early_bird: bool,
        is_member: bool,
        can_book_date: date
    ) -> int:
        """
        新增預約訂票記錄
        
        Args:
            user_id: 訂票人ID
            ticket_type: 票券類型 (e.g., "THSR")
            adult_count: 成人數量
            child_count: 兒童數量
            student_count: 學生數量
            elder_count: 敬老票數量
            disabled_count: 身障票數量
            booking_date: 搭乘日期
            booking_time: 搭乘時間
            start_station: 上車站
            end_station: 下車站
            is_early_bird: 是否為早鳥票
            is_member: 是否為會員
            can_book_date: 可以完成訂票的日期
            
        Returns:
            int: 新建立的booking_id
            
        Raises:
            SQLAlchemyError: 數據庫操作錯誤
        """
        try:
            # 生成ticket_number (簡單實現: user_id + 時間戳)
            ticket_number = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 建立新的BookingTicket記錄
            booking = BookingTicket(
                user_id=user_id,
                adult_count=adult_count,
                child_count=child_count,
                student_count=student_count,
                elder_count=elder_count,
                disabled_count=disabled_count,
                ticket_type=ticket_type,
                ticket_number=ticket_number,
                booking_date=booking_date,
                booking_time=booking_time,
                start_station=start_station,
                end_station=end_station,
                is_early_bird=is_early_bird,
                is_member=is_member,
                can_book_date=can_book_date
            )
            
            # 新增到session
            self.db.add(booking)
            # 刷新以獲取自動生成的ID
            self.db.flush()
            
            booking_id = booking.booking_id
            
            # 提交事務
            self.db.commit()
            
            return booking_id
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"新增預約訂票記錄失敗: {str(e)}")
    
    def create_early_bird(self, booking_id: int, user_id: str) -> int:
        """
        新增早鳥票使用者
        
        Args:
            booking_id: 預約訂票ID
            user_id: 早鳥票使用者ID
            
        Returns:
            int: 新建立的early_bird_id
            
        Raises:
            SQLAlchemyError: 數據庫操作錯誤
        """
        try:
            # 建立新的EarlyBird記錄
            early_bird = EarlyBird(
                booking_id=booking_id,
                user_id=user_id
            )
            
            # 新增到session
            self.db.add(early_bird)
            # 刷新以獲取自動生成的ID
            self.db.flush()
            
            early_bird_id = early_bird.early_bird_id
            
            # 提交事務
            self.db.commit()
            
            return early_bird_id
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"新增早鳥票記錄失敗: {str(e)}")
