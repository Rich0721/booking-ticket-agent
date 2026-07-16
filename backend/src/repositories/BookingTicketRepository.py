from datetime import datetime, date


class BookingTicketRepository:
    """預約訂票資料庫操作"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
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
            (所有預約訂票相關參數)
            
        Returns:
            booking_id
        """
        # TODO: 實際資料庫操作實現
        # 這裡返回mock的booking_id用於測試
        return 1
    
    def create_early_bird(self, booking_id: int, user_id: str) -> int:
        """
        新增早鳥票使用者
        
        Args:
            booking_id: 預約訂票ID
            user_id: 使用者ID
            
        Returns:
            early_bird_id
        """
        # TODO: 實際資料庫操作實現
        # 這裡返回mock的early_bird_id用於測試
        return 1
