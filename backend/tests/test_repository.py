"""
預約訂票Repository單元測試

測試BookingTicketRepository的create_booking和create_early_bird方法
"""

import pytest
from datetime import date, time
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session

from src.repositories.BookingTicketRepository import BookingTicketRepository
from src.objects.models.booking_ticket_models import BookingTicket, EarlyBird


class TestBookingTicketRepository:
    """預約訂票Repository測試"""
    
    @pytest.fixture
    def mock_db_session(self):
        """建立模擬的SQLAlchemy Session"""
        session = MagicMock(spec=Session)
        session._booking_id_counter = 1
        session._early_bird_id_counter = 1
        
        def add_side_effect(obj):
            """模擬add方法為對象分配ID"""
            if isinstance(obj, BookingTicket):
                if obj.booking_id is None:
                    obj.booking_id = session._booking_id_counter
                    session._booking_id_counter += 1
            elif isinstance(obj, EarlyBird):
                if obj.early_bird_id is None:
                    obj.early_bird_id = session._early_bird_id_counter
                    session._early_bird_id_counter += 1
        
        session.add.side_effect = add_side_effect
        session.flush = Mock()
        session.commit = Mock()
        session.rollback = Mock()
        
        return session
    
    @pytest.fixture
    def repository(self, mock_db_session):
        """建立Repository實例"""
        return BookingTicketRepository(mock_db_session)
    
    def test_create_booking_success(self, repository, mock_db_session):
        """測試成功新增預約訂票 - Scenario: 新增預約訂票成功"""
        # 準備測試數據
        user_id = "A123456785"
        ticket_type = "THSR"
        
        # 執行
        booking_id = repository.create_booking(
            user_id=user_id,
            ticket_type=ticket_type,
            adult_count=2,
            child_count=1,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            booking_date=date(2026, 7, 21),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            is_early_bird=False,
            is_member=False,
            can_book_date=date(2026, 7, 2)
        )
        
        # 驗證
        assert booking_id == 1
        # 驗證add被調用
        assert mock_db_session.add.called
        # 驗證flush和commit被調用
        assert mock_db_session.flush.called
        assert mock_db_session.commit.called
        # 驗證rollback未被調用（成功情況）
        assert not mock_db_session.rollback.called
    
    def test_create_booking_multiple(self, repository, mock_db_session):
        """測試多次新增預約訂票 - Scenario: 連續新增多筆預約"""
        # 執行多次調用
        booking_id_1 = repository.create_booking(
            user_id="A123456785",
            ticket_type="THSR",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            booking_date=date(2026, 7, 21),
            booking_time="10:30",
            start_station="台北",
            end_station="左營",
            is_early_bird=False,
            is_member=False,
            can_book_date=date(2026, 7, 2)
        )
        
        booking_id_2 = repository.create_booking(
            user_id="B287654325",
            ticket_type="THSR",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            booking_date=date(2026, 8, 3),
            booking_time="14:00",
            start_station="台中",
            end_station="高雄",
            is_early_bird=False,
            is_member=True,
            can_book_date=date(2026, 7, 5)
        )
        
        # 驗證ID遞增
        assert booking_id_1 == 1
        assert booking_id_2 == 2
    
    def test_create_early_bird_success(self, repository, mock_db_session):
        """測試成功新增早鳥票 - Scenario: 新增早鳥票使用者成功"""
        # 執行
        early_bird_id = repository.create_early_bird(
            booking_id=1,
            user_id="A123456785"
        )
        
        # 驗證
        assert early_bird_id == 1
        # 驗證add被調用
        assert mock_db_session.add.called
        # 驗證flush和commit被調用
        assert mock_db_session.flush.called
        assert mock_db_session.commit.called
        # 驗證rollback未被調用（成功情況）
        assert not mock_db_session.rollback.called
    
    def test_create_early_bird_multiple(self, repository, mock_db_session):
        """測試多次新增早鳥票 - Scenario: 同一筆預約新增多個早鳥票"""
        # 執行多次調用
        early_bird_id_1 = repository.create_early_bird(
            booking_id=1,
            user_id="A123456785"
        )
        
        early_bird_id_2 = repository.create_early_bird(
            booking_id=1,
            user_id="B287654325"
        )
        
        # 驗證ID遞增
        assert early_bird_id_1 == 1
        assert early_bird_id_2 == 2
    
    @pytest.mark.parametrize("user_id,booking_id", [
        ("A123456785", 1),
        ("B287654325", 2),
        ("C111111111", 3),
    ])
    def test_create_early_bird_parametrized(self, repository, mock_db_session, user_id, booking_id):
        """測試早鳥票用不同用戶ID - Scenario: 多個用戶的早鳥票"""
        early_bird_id = repository.create_early_bird(
            booking_id=booking_id,
            user_id=user_id
        )
        
        assert early_bird_id >= 1
        assert mock_db_session.add.called
        assert mock_db_session.commit.called
    
    def test_create_booking_with_database_error(self, repository, mock_db_session):
        """測試新增預約訂票時數據庫錯誤 - Scenario: 數據庫操作失敗"""
        # 設置flush拋出異常
        from sqlalchemy.exc import SQLAlchemyError
        mock_db_session.flush.side_effect = SQLAlchemyError("Database connection error")
        
        # 驗證拋出異常
        with pytest.raises(Exception, match="新增預約訂票記錄失敗"):
            repository.create_booking(
                user_id="A123456785",
                ticket_type="THSR",
                adult_count=1,
                child_count=0,
                student_count=0,
                elder_count=0,
                disabled_count=0,
                booking_date=date(2026, 7, 21),
                booking_time="10:30",
                start_station="台北",
                end_station="左營",
                is_early_bird=False,
                is_member=False,
                can_book_date=date(2026, 7, 2)
            )
        
        # 驗證rollback被調用
        assert mock_db_session.rollback.called
    
    def test_create_early_bird_with_database_error(self, repository, mock_db_session):
        """測試新增早鳥票時數據庫錯誤 - Scenario: 早鳥票數據庫操作失敗"""
        # 設置flush拋出異常
        from sqlalchemy.exc import SQLAlchemyError
        mock_db_session.flush.side_effect = SQLAlchemyError("Database connection error")
        
        # 驗證拋出異常
        with pytest.raises(Exception, match="新增早鳥票記錄失敗"):
            repository.create_early_bird(
                booking_id=1,
                user_id="A123456785"
            )
        
        # 驗證rollback被調用
        assert mock_db_session.rollback.called
