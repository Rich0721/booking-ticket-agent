"""
Driver超時處理測試
來源：Requirement - Driver卡住處理
- 場景1: Driver超時自動重啟
- 場景2: 第一次失敗加入Retry列表
- 場景3: 第二次失敗直接標記為"Booking Error"
"""

import pytest
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from src.utils.DriverTimeoutManager import DriverTimeoutManager


class TestDriverTimeoutManager:
    """Driver超時管理器測試"""
    
    def test_timeout_manager_initialization(self):
        """
        場景1: 超時管理器初始化
        來源：Requirement - Driver卡住處理
        """
        manager = DriverTimeoutManager(timeout_seconds=5.0)
        
        assert manager.timeout_seconds == 5.0
        assert not manager.is_timeout()
    
    def test_timeout_manager_start_and_stop(self):
        """
        場景2: 超時管理器啟動和停止
        來源：Requirement - Driver卡住處理
        """
        manager = DriverTimeoutManager(timeout_seconds=1.0)
        
        manager.start()
        time.sleep(0.1)
        assert not manager.is_timeout()
        
        manager.stop()
        time.sleep(0.1)
    
    def test_timeout_detection(self):
        """
        場景3: 超時檢測
        如果卡住超過一定時間，則標記為超時
        來源：Requirement - Driver卡住處理
        """
        manager = DriverTimeoutManager(timeout_seconds=0.5)
        manager.start()
        
        # 等待超時（需要比超時時間更長，再加上watchdog檢查間隔）
        time.sleep(2.0)
        assert manager.is_timeout()
        
        manager.stop()
    
    def test_reset_activity_clears_timeout(self):
        """
        場景4: 重置活動時間戳會清除超時狀態
        來源：Requirement - Driver卡住處理
        """
        manager = DriverTimeoutManager(timeout_seconds=0.5)
        manager.start()
        
        # 等待接近超時但不超時
        time.sleep(0.3)
        assert not manager.is_timeout()
        
        # 重置活動時間戳
        manager.reset_activity()
        time.sleep(0.3)
        assert not manager.is_timeout()
        
        manager.stop()
    
    def test_timeout_callback_execution(self):
        """
        場景5: 超時時執行回調函數
        如果卡住超過一定時間，則自動重啟Driver
        來源：Requirement - Driver卡住處理
        """
        callback_mock = Mock()
        manager = DriverTimeoutManager(timeout_seconds=0.3)
        manager.set_timeout_callback(callback_mock)
        manager.start()
        
        # 等待超時和回調執行
        time.sleep(2.0)
        
        # 檢查回調是否被執行
        callback_mock.assert_called()
        
        manager.stop()
    
    def test_timeout_callback_exception_handling(self):
        """
        場景6: 超時回調異常處理
        即使回調出錯，超時管理器應該繼續運行
        來源：Requirement - Driver卡住處理
        """
        def failing_callback():
            raise RuntimeError("Callback failed")
        
        manager = DriverTimeoutManager(timeout_seconds=0.3)
        manager.set_timeout_callback(failing_callback)
        manager.start()
        
        # 等待超時和回調執行（即使回調失敗）
        time.sleep(2.0)
        
        # 檢查超時狀態
        assert manager.is_timeout()
        
        manager.stop()
    
    def test_multiple_reset_activities(self):
        """
        場景7: 多次重置活動時間戳
        來源：Requirement - Driver卡住處理
        """
        manager = DriverTimeoutManager(timeout_seconds=0.5)
        manager.start()
        
        for _ in range(3):
            time.sleep(0.3)
            manager.reset_activity()
            assert not manager.is_timeout()
        
        # 停止重置，等待超時
        time.sleep(2.0)
        assert manager.is_timeout()
        
        manager.stop()
    
    def test_custom_timeout_duration(self):
        """
        場景8: 自訂超時時間
        來源：Requirement - Driver卡住處理
        """
        manager_short = DriverTimeoutManager(timeout_seconds=0.3)
        manager_long = DriverTimeoutManager(timeout_seconds=2.0)
        
        manager_short.start()
        manager_long.start()
        
        time.sleep(1.0)
        
        # 短超時應該已經超時
        assert manager_short.is_timeout()
        # 長超時不應該超時
        assert not manager_long.is_timeout()
        
        manager_short.stop()
        manager_long.stop()
