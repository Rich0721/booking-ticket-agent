from typing import List, Optional

from sqlalchemy.orm import Session

from src.objects.models.booking_ticket_models import SystemParam


class SelectionRepository:
    """系統選項資料庫操作"""

    def __init__(self, db_session: Optional[Session] = None):
        self.db = db_session

    def get_by_category(self, parm_category: str) -> List[SystemParam]:
        """依類別查詢選單資料"""
        if self.db is None:
            return []
        return (
            self.db.query(SystemParam)
            .filter(SystemParam.parm_category == parm_category)
            .order_by(SystemParam.parm_id.asc())
            .all()
        )
