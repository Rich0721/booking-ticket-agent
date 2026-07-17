"""
pytest配置文件和公共fixtures
"""

import pytest
import os
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# 載入測試環境變數
load_dotenv(os.path.join(os.path.dirname(__file__), "../env/.env.dev"))


@pytest.fixture
def mock_db_session():
    """
    建立模擬的SQLAlchemy Session
    
    用於測試Repository的數據庫操作，而不實際連接真實數據庫
    """
    session = MagicMock(spec=Session)
    
    # 配置預設行為
    # flush()和commit()不執行任何操作，僅用於測試驗證
    session.flush = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    session.add = Mock()
    
    # 配置booking ID計數器
    session._booking_id_counter = 1
    session._early_bird_id_counter = 1
    
    def add_side_effect(obj):
        """模擬add方法的行為"""
        # 檢查對象類型並分配ID
        if hasattr(obj, 'booking_id'):
            # 如果是BookingTicket對象
            if obj.booking_id is None:
                obj.booking_id = session._booking_id_counter
                session._booking_id_counter += 1
        elif hasattr(obj, 'early_bird_id'):
            # 如果是EarlyBird對象
            if obj.early_bird_id is None:
                obj.early_bird_id = session._early_bird_id_counter
                session._early_bird_id_counter += 1
    
    session.add.side_effect = add_side_effect
    
    yield session
