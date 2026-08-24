import pytest
from datetime import date, time
from unittest.mock import Mock, patch, MagicMock
from src.services.BookingTicketService import BookingTicketService
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo
from src.repositories.BookingTicketRepository import BookingTicketRepository
from src.utils.booking_utils import (
    parse_train_schedules, find_best_train, extract_pnr_code,
    DEPARTURE_TIME_KEY, TRAIN_NO_KEY, ARRIVAL_TIME_KEY, DEPARTURE_DATE_KEY
)


class TestBookingTicketService:
    """訂票服務單元測試"""
    
    @pytest.fixture
    def mock_repository(self):
        """Mock數據庫倉儲"""
        return Mock(spec=BookingTicketRepository)
    
    @pytest.fixture
    def booking_service(self, mock_repository):
        """訂票服務實例"""
        service = BookingTicketService()
        service.repository = mock_repository
        return service
    
    @pytest.fixture
    def sample_booking_info(self):
        """樣本訂票資訊"""
        return CBookingTicketInfo(
            booking_id=1,
            user_id="A123456789",
            adult_count=1,
            child_count=0,
            student_count=0,
            elder_count=0,
            disabled_count=0,
            ticket_type="THSR",
            booking_date=date(2026, 8, 25),
            booking_time=time(14, 30),
            start_station="台北",
            end_station="左營",
            is_early_bird=False,
            is_member=False,
            can_book_date=date(2026, 8, 24),
            ticket_number=None,
            early_bird_ids=[]
        )
    
    def test_process_daily_bookings_no_records(self, booking_service, mock_repository):
        """場景2: 測試無待訂票記錄"""
        # 模擬無訂票記錄
        mock_repository.get_booking_tickets_by_can_book_date.return_value = []
        
        # 執行
        successful, failed = booking_service.process_daily_bookings(date(2026, 8, 24))
        
        # 驗證
        assert successful == 0
        assert failed == 0
        mock_repository.get_booking_tickets_by_can_book_date.assert_called_once()
    
    def test_process_daily_bookings_multiple_records(self, booking_service, mock_repository, sample_booking_info):
        """場景3: 測試多筆訂票記錄"""
        # 建立多筆訂票記錄
        bookings = [sample_booking_info] * 5
        mock_repository.get_booking_tickets_by_can_book_date.return_value = bookings
        
        # 模擬single booking結果
        with patch.object(booking_service, '_process_single_booking', return_value=True):
            # 執行
            successful, failed = booking_service.process_daily_bookings(date(2026, 8, 24))
            
            # 驗證
            assert successful == 5
            assert failed == 0
    
    def test_process_daily_bookings_with_failures(self, booking_service, mock_repository, sample_booking_info):
        """場景4: 測試訂票失敗重試"""
        # 建立訂票記錄
        bookings = [sample_booking_info, sample_booking_info]
        mock_repository.get_booking_tickets_by_can_book_date.return_value = bookings
        
        # 模擬：第一筆成功，第二筆失敗
        with patch.object(booking_service, '_process_single_booking', side_effect=[True, False]):
            # 執行
            successful, failed = booking_service.process_daily_bookings(date(2026, 8, 24))
            
            # 驗證
            assert successful == 1
            assert failed == 1
            mock_repository.update_ticket_number.assert_called()


class TestBookingUtils:
    """訂票工具函數測試"""
    
    def test_parse_train_schedules_valid_html(self):
        """測試解析列車時刻表 - 有效HTML"""
        # 建立樣本HTML
        html = """
        <div id="BookingS2Form_TrainQueryDataViewPanel">
            <div class="result-listing">
                <label class="result-item">
                    <input class="uk-radio" querycode="801" querydeparture="06:00" 
                           queryarrival="07:30" queryestimatedtime="1:30" querydeparturedate="08/25" />
                </label>
                <label class="result-item">
                    <input class="uk-radio" querycode="803" querydeparture="07:00" 
                           queryarrival="08:30" queryestimatedtime="1:30" querydeparturedate="08/25" />
                </label>
            </div>
        </div>
        """
        
        # 執行
        schedules = parse_train_schedules(html)
        
        # 驗證
        assert len(schedules) == 2
        assert schedules[0][TRAIN_NO_KEY] == "801"
        assert schedules[1][TRAIN_NO_KEY] == "803"
        assert schedules[0][DEPARTURE_TIME_KEY] == "06:00"
    
    def test_parse_train_schedules_empty_html(self):
        """測試解析列車時刻表 - 空HTML"""
        html = "<div></div>"
        
        # 執行
        schedules = parse_train_schedules(html)
        
        # 驗證
        assert len(schedules) == 0
    
    @pytest.mark.parametrize(
        "target_time,is_early_bird,expected_departure",
        [
            ("06:30", False, "06:00"),  # 選擇最接近的非早鳥車次
            ("07:30", False, "07:00"),  # 選擇最接近的非早鳥車次
        ]
    )
    def test_find_best_train_no_early_bird(self, target_time, is_early_bird, expected_departure):
        """場景5: 測試選擇最佳列車"""
        schedules = [
            {
                TRAIN_NO_KEY: "801",
                DEPARTURE_TIME_KEY: "06:00",
                ARRIVAL_TIME_KEY: "07:30",
                DEPARTURE_DATE_KEY: "08/25",
                'EARLY_BIRD': ''
            },
            {
                TRAIN_NO_KEY: "803",
                DEPARTURE_TIME_KEY: "07:00",
                ARRIVAL_TIME_KEY: "08:30",
                DEPARTURE_DATE_KEY: "08/25",
                'EARLY_BIRD': ''
            },
        ]
        
        # 執行
        selected_train = find_best_train(schedules, target_time, is_early_bird)
        
        # 驗證
        assert selected_train is not None
        assert selected_train[DEPARTURE_TIME_KEY] == expected_departure
    
    def test_extract_pnr_code_valid_html(self):
        """測試提取訂單代號 - 有效HTML"""
        html = """
        <div class="pnr-code">
            <span>1234567890</span>
        </div>
        """
        
        # 執行
        pnr_code = extract_pnr_code(html)
        
        # 驗證
        assert pnr_code == "1234567890"
    
    def test_extract_pnr_code_invalid_html(self):
        """測試提取訂單代號 - 無效HTML"""
        html = "<div></div>"
        
        # 執行
        pnr_code = extract_pnr_code(html)
        
        # 驗證
        assert pnr_code is None


class TestBookingTicketRepository:
    """訂票資訊數據庫操作單元測試"""
    
    @patch('src.repositories.BookingTicketRepository.DatabaseConfig')
    def test_get_booking_tickets_by_can_book_date(self, mock_db_config_class):
        """測試查詢指定日期的待訂票記錄"""
        # 建立mock實例
        repo = BookingTicketRepository()
        
        # 設置mock連接
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        repo.db_config = MagicMock()
        repo.db_config.get_connection.return_value.__enter__.return_value = mock_conn
        repo.db_config.get_connection.return_value.__exit__.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        
        # 模擬查詢結果
        mock_cursor.fetchall.return_value = [
            (1, "A123456789", 1, 0, 0, 0, 0, "THSR", date(2026, 8, 25), 
             time(14, 30), "台北", "左營", False, False, date(2026, 8, 24), None)
        ]
        
        # Mock早鳥票查詢
        with patch.object(repo, 'get_early_bird_info', return_value=[]):
            # 執行
            bookings = repo.get_booking_tickets_by_can_book_date(date(2026, 8, 24))
            
            # 驗證
            assert len(bookings) == 1
            assert bookings[0].booking_id == 1
            assert bookings[0].user_id == "A123456789"
    
    @patch('src.repositories.BookingTicketRepository.DatabaseConfig')
    def test_update_ticket_number(self, mock_db_config_class):
        """測試更新訂單代號"""
        # 建立mock實例
        repo = BookingTicketRepository()
        
        # 設置mock連接
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        repo.db_config = MagicMock()
        repo.db_config.get_connection.return_value.__enter__.return_value = mock_conn
        repo.db_config.get_connection.return_value.__exit__.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        
        # 執行
        success = repo.update_ticket_number(1, "1234567890")
        
        # 驗證
        assert success is True
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
