from datetime import date
from typing import List, Optional, Tuple
from src.config.database import DatabaseConfig
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo


class BookingTicketRepository:
    """訂票資訊數據庫操作類"""
    
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def get_booking_tickets_by_can_book_date(self, can_book_date: date) -> List[CBookingTicketInfo]:
        """
        查詢指定日期可訂票的所有訂票記錄
        
        Args:
            can_book_date: 可訂票日期
            
        Returns:
            訂票記錄列表
        """
        try:
            with self.db_config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT BOOKING_ID, USER_ID, ADULT_COUNT, CHILD_COUNT, STUDENT_COUNT, 
                           ELDER_COUNT, DISABLED_COUNT, TICKET_TYPE, BOOKING_DATE, BOOKING_TIME,
                           START_STATION, END_STATION, IS_EARLY_BIRD, IS_MEMBER, CAN_BOOK_DATE, 
                           TICKET_NUMBER
                    FROM TB_BOOKING_TICKET
                    WHERE CAN_BOOK_DATE = %s AND TICKET_NUMBER IS NULL
                    ORDER BY BOOKING_ID ASC
                    """,
                    (can_book_date,)
                )
                
                rows = cursor.fetchall()
                booking_tickets = []
                
                for row in rows:
                    booking_tickets.append(self._row_to_booking_ticket_info(row))
                
                return booking_tickets
        except Exception as e:
            print(f"查詢訂票記錄失敗: {str(e)}")
            return []
    
    def get_early_bird_info(self, booking_id: int) -> List[str]:
        """
        查詢指定訂票ID的早鳥票乘客資訊
        
        Args:
            booking_id: 訂票ID
            
        Returns:
            早鳥票乘客ID列表
        """
        try:
            with self.db_config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT USER_ID
                    FROM TB_EARLY_BIRD
                    WHERE BOOKING_ID = %s
                    ORDER BY EARLY_BIRD_ID ASC
                    """,
                    (booking_id,)
                )
                
                rows = cursor.fetchall()
                return [row[0] for row in rows]
        except Exception as e:
            print(f"查詢早鳥票乘客資訊失敗: {str(e)}")
            return []
    
    def update_ticket_number(self, booking_id: int, ticket_number: str) -> bool:
        """
        更新訂票記錄的訂單代號
        
        Args:
            booking_id: 訂票ID
            ticket_number: 訂單代號
            
        Returns:
            是否更新成功
        """
        try:
            with self.db_config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE TB_BOOKING_TICKET
                    SET TICKET_NUMBER = %s, UPDATED_TIME = NOW()
                    WHERE BOOKING_ID = %s
                    """,
                    (ticket_number, booking_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"更新訂單代號失敗: {str(e)}")
            return False
    
    def _row_to_booking_ticket_info(self, row: Tuple) -> CBookingTicketInfo:
        """
        將數據庫行轉換為訂票資訊對象
        
        Args:
            row: 數據庫查詢結果行
            
        Returns:
            訂票資訊對象
        """
        booking_ids = self._get_early_bird_ids(row[0])
        
        return CBookingTicketInfo(
            booking_id=row[0],
            user_id=row[1],
            adult_count=row[2],
            child_count=row[3],
            student_count=row[4],
            elder_count=row[5],
            disabled_count=row[6],
            ticket_type=row[7],
            booking_date=row[8],
            booking_time=row[9],
            start_station=row[10],
            end_station=row[11],
            is_early_bird=row[12],
            is_member=row[13],
            can_book_date=row[14],
            ticket_number=row[15],
            early_bird_ids=booking_ids
        )
    
    def _get_early_bird_ids(self, booking_id: int) -> List[str]:
        """
        獲取指定訂票ID的所有早鳥票乘客ID
        
        Args:
            booking_id: 訂票ID
            
        Returns:
            早鳥票乘客ID列表
        """
        return self.get_early_bird_info(booking_id)
