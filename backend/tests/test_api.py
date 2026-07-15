"""API整合測試 - 來源: Booking_Ticket.feature, Search_Ticket.feature, Delete_Ticket.feature"""
import unittest
import json
from unittest.mock import patch, MagicMock
from src.main import app

class TestBookingAPI(unittest.TestCase):
    """預約訂票API測試類別"""
    
    def setUp(self):
        """設置測試環境"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('src.api.booking_api.Database')
    def test_booking_ticket_success_within_29_days(self, mock_db_class):
        """
        測試成功預約訂票（29天內）
        
        來源: Booking_Ticket.feature Rule: 搭乘日在系統日起29天內
        - 系統日為 "2026/07/01"
        - 搭乘日 "2026/07/03"
        - 期望: 回傳訊息包含 "2026/07/02將完成訂票"
        """
        # 設置Mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_db.fetch_one.return_value = {'id': 1}
        
        payload = {
            "info": {
                "user_id": "A123456789",
                "ticket_type": "THSR",
                "booking_date": "2026-07-03",
                "booking_time": "10:30",
                "start_station": "台北",
                "end_station": "左營",
                "adults": 1,
                "childs": 0,
                "students": 0,
                "elders": 0,
                "disables": 0,
                "is_early_bird": False,
                "is_member": True,
                "early_ids": []
            }
        }
        
        response = self.client.post('/booking-ticket', 
                                   data=json.dumps(payload),
                                   content_type='application/json',
                                   headers={'X-System-Date': '2026-07-01'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('2026/07/02', data['headers']['message'])
        self.assertIn('將完成訂票', data['headers']['message'])
    
    @patch('src.api.booking_api.Database')
    def test_booking_ticket_invalid_id(self, mock_db_class):
        """
        測試無效身份證的預約訂票
        
        來源: Booking_Ticket.feature Rule: 訂票人ID與早鳥票ID共用同一個檢查方式
        """
        payload = {
            "info": {
                "user_id": "1234567890",  # 無效的身份證
                "ticket_type": "THSR",
                "booking_date": "2026-07-03",
                "booking_time": "10:30",
                "start_station": "台北",
                "end_station": "左營",
                "adults": 1,
                "childs": 0,
                "students": 0,
                "elders": 0,
                "disables": 0,
                "is_early_bird": False,
                "is_member": True,
                "early_ids": []
            }
        }
        
        response = self.client.post('/booking-ticket',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('身份證', data['headers']['message'])
    
    @patch('src.api.booking_api.Database')
    def test_booking_ticket_early_bird_mismatch(self, mock_db_class):
        """
        測試早鳥票ID數量不符
        
        來源: Booking_Ticket.feature III. 需求說明: 早鳥票ID數量須與全票(Adults)相同
        """
        payload = {
            "info": {
                "user_id": "A123456789",
                "ticket_type": "THSR",
                "booking_date": "2026-07-03",
                "booking_time": "10:30",
                "start_station": "台北",
                "end_station": "左營",
                "adults": 2,
                "childs": 0,
                "students": 0,
                "elders": 0,
                "disables": 0,
                "is_early_bird": True,
                "is_member": True,
                "early_ids": ["A123456789"]  # 數量應為2
            }
        }
        
        response = self.client.post('/booking-ticket',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('早鳥票ID', data['headers']['message'])
    
    @patch('src.api.booking_api.Database')
    def test_booking_ticket_same_day_not_allowed(self, mock_db_class):
        """
        測試當天預約不接受
        
        來源: Booking_Ticket.feature Rule: 搭乘日為當日或過去不可預約
        """
        payload = {
            "info": {
                "user_id": "A123456789",
                "ticket_type": "THSR",
                "booking_date": "2026-07-01",  # 當天
                "booking_time": "10:30",
                "start_station": "台北",
                "end_station": "左營",
                "adults": 1,
                "childs": 0,
                "students": 0,
                "elders": 0,
                "disables": 0,
                "is_early_bird": False,
                "is_member": True,
                "early_ids": []
            }
        }
        
        response = self.client.post('/booking-ticket',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('當天不接受預約訂票', data['headers']['message'])


class TestSearchAPI(unittest.TestCase):
    """查詢訂票API測試類別"""
    
    def setUp(self):
        """設置測試環境"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('src.api.search_api.Database')
    def test_search_booking_success(self, mock_db_class):
        """
        測試成功查詢訂票資訊
        
        來源: Search_Ticket.feature Rule: 系統應依查詢條件顯示使用者的訂票資料
        """
        # 設置Mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        # 模擬資料庫結果
        from datetime import date, time
        mock_db.fetch_all.return_value = [
            {
                'id': 1,
                'booking_date': date(2026, 7, 4),
                'booking_time': time(22, 0),
                'start_station': '左營',
                'end_station': '南港',
                'ticket_number': 'AD1321'
            },
            {
                'id': 2,
                'booking_date': date(2026, 8, 10),
                'booking_time': time(22, 0),
                'start_station': '左營',
                'end_station': '南港',
                'ticket_number': None
            }
        ]
        
        payload = {
            "info": {
                "user_id": "A123456789",
                "ticket_type": "THSR"
            }
        }
        
        response = self.client.post('/search-booking-ticket',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['info']['booking_info']), 2)
        self.assertEqual(data['info']['booking_info'][0]['ticket_number'], 'AD1321')
        self.assertFalse(data['info']['booking_info'][0]['canDelete'])
        self.assertEqual(data['info']['booking_info'][1]['ticket_number'], '')
        self.assertTrue(data['info']['booking_info'][1]['canDelete'])
    
    @patch('src.api.search_api.Database')
    def test_search_booking_no_result(self, mock_db_class):
        """
        測試查詢無結果
        
        來源: Search_Ticket.feature Example:使用者未有預約資訊
        """
        # 設置Mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_db.fetch_all.return_value = []
        
        payload = {
            "info": {
                "user_id": "A123456789",
                "ticket_type": "THSR"
            }
        }
        
        response = self.client.post('/search-booking-ticket',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['info']['booking_info']), 0)


class TestDeleteAPI(unittest.TestCase):
    """刪除訂票API測試類別"""
    
    def setUp(self):
        """設置測試環境"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('src.api.delete_api.Database')
    def test_delete_booking_success(self, mock_db_class):
        """
        測試成功刪除訂票（無取票號碼）
        
        來源: Delete_Ticket.feature Example: 使用者刪除未含有取票號碼的訂票資訊
        """
        # 設置Mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        # 模擬查詢結果
        mock_db.fetch_one.return_value = {
            'TICKET_NUMBER': None,
            'USER_ID': 'A123456789',
            'TICKET_TYPE': 'THSR'
        }
        
        # 模擬刪除後的查詢結果
        from datetime import date, time
        mock_db.fetch_all.return_value = [
            {
                'id': 1,
                'booking_date': date(2026, 7, 4),
                'booking_time': time(22, 0),
                'start_station': '左營',
                'end_station': '南港',
                'ticket_number': 'AD1321'
            }
        ]
        
        response = self.client.delete('/delete-booking-ticket/2')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('已成功刪除', data['headers']['message'])
    
    @patch('src.api.delete_api.Database')
    def test_delete_booking_with_ticket_number(self, mock_db_class):
        """
        測試刪除已完成訂票的資訊（含取票號碼）
        
        來源: Delete_Ticket.feature Example: 使用者刪除含有取票號碼的訂票資訊
        """
        # 設置Mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        # 模擬查詢結果
        mock_db.fetch_one.return_value = {
            'TICKET_NUMBER': 'AD1321',  # 已有取票號碼
            'USER_ID': 'A123456789',
            'TICKET_TYPE': 'THSR'
        }
        
        response = self.client.delete('/delete-booking-ticket/1')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('該資料已完成訂票', data['headers']['message'])


class TestMenuAPI(unittest.TestCase):
    """載入選單API測試類別"""
    
    def setUp(self):
        """設置測試環境"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('src.api.menu_api.Database')
    def test_loading_selected_success(self, mock_db_class):
        """
        測試成功載入選單
        
        來源: Loading_Selected.md III. 需求說明
        """
        # 設置Mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        # 模擬資料庫結果
        mock_db.fetch_all.return_value = [
            {
                'id': 1,
                'parm_name': '首頁',
                'parm_value': 'home'
            },
            {
                'id': 2,
                'parm_name': '訂票',
                'parm_value': 'booking'
            }
        ]
        
        response = self.client.get('/loading-selected?parm_category=menu')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['info']['menu']), 2)
        self.assertEqual(data['info']['menu'][0]['parm_name'], '首頁')
        self.assertEqual(data['info']['menu'][0]['parm_value'], 'home')
    
    def test_loading_selected_missing_parameter(self):
        """
        測試缺少必要參數
        
        來源: Loading_Selected.md IV. 其它說明
        """
        response = self.client.get('/loading-selected')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('parm_category', data['headers']['message'])


if __name__ == '__main__':
    unittest.main()
