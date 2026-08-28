"""
CWebDriver超時功能測試
來源：Requirement - Driver卡住處理
- 場景1: WebDriver創建時啟用超時監控
- 場景2: WebDriver關閉時停止超時監控
- 場景3: 檢測Driver超時狀態
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.objects.classes.CWebDriver import CWebDriver
from src.utils.DriverTimeoutManager import DriverTimeoutManager


class TestCWebDriverTimeout:
    """CWebDriver超時功能測試"""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """重置單例實例"""
        CWebDriver._CWebDriver__instance = None
        yield
        if CWebDriver._CWebDriver__instance:
            try:
                CWebDriver._CWebDriver__instance.close_driver()
            except:
                pass
            CWebDriver._CWebDriver__instance = None
    
    @patch('src.objects.classes.CWebDriver.webdriver.Edge')
    def test_create_driver_with_timeout_enabled(self, mock_edge):
        """
        場景1: WebDriver創建時啟用超時監控
        如果卡住超過一定時間，則自動重啟Driver
        來源：Requirement - Driver卡住處理
        """
        mock_driver_instance = MagicMock()
        mock_edge.return_value = mock_driver_instance
        
        manager = CWebDriver.get_instance()
        driver = manager.create_driver(enable_timeout=True)
        
        assert driver is not None
        assert manager._CWebDriver__timeout_manager is not None
        assert isinstance(manager._CWebDriver__timeout_manager, DriverTimeoutManager)
    
    @patch('src.objects.classes.CWebDriver.webdriver.Edge')
    def test_create_driver_without_timeout(self, mock_edge):
        """
        場景2: WebDriver創建時不啟用超時監控
        來源：Requirement - Driver卡住處理
        """
        mock_driver_instance = MagicMock()
        mock_edge.return_value = mock_driver_instance
        
        manager = CWebDriver.get_instance()
        driver = manager.create_driver(enable_timeout=False)
        
        assert driver is not None
        assert manager._CWebDriver__timeout_manager is None
    
    @patch('src.objects.classes.CWebDriver.webdriver.Edge')
    def test_reset_activity(self, mock_edge):
        """
        場景3: 重置活動時間戳
        來源：Requirement - Driver卡住處理
        """
        mock_driver_instance = MagicMock()
        mock_edge.return_value = mock_driver_instance
        
        manager = CWebDriver.get_instance()
        driver = manager.create_driver(enable_timeout=True)
        
        # 重置活動時間戳
        manager.reset_activity()
        
        # 檢查超時管理器是否被重置
        assert not manager.is_driver_timeout()
    
    @patch('src.objects.classes.CWebDriver.webdriver.Edge')
    def test_is_driver_timeout(self, mock_edge):
        """
        場景4: 檢測Driver超時狀態
        來源：Requirement - Driver卡住處理
        """
        mock_driver_instance = MagicMock()
        mock_edge.return_value = mock_driver_instance
        
        manager = CWebDriver.get_instance()
        driver = manager.create_driver(enable_timeout=True)
        
        # 檢查超時狀態
        assert not manager.is_driver_timeout()
    
    @patch('src.objects.classes.CWebDriver.webdriver.Edge')
    def test_close_driver_stops_timeout_monitor(self, mock_edge):
        """
        場景5: 關閉WebDriver時停止超時監控
        來源：Requirement - Driver卡住處理
        """
        mock_driver_instance = MagicMock()
        mock_edge.return_value = mock_driver_instance
        
        manager = CWebDriver.get_instance()
        driver = manager.create_driver(enable_timeout=True)
        
        timeout_manager = manager._CWebDriver__timeout_manager
        assert timeout_manager is not None
        
        manager.close_driver()
        
        # 檢查超時管理器是否被停止
        assert manager._CWebDriver__timeout_manager is None
    
    @patch('src.objects.classes.CWebDriver.webdriver.Edge')
    def test_create_new_driver_closes_previous(self, mock_edge):
        """
        場景6: 創建新Driver時關閉舊Driver
        來源：Requirement - Driver卡住處理
        """
        mock_driver_instance1 = MagicMock()
        mock_driver_instance2 = MagicMock()
        mock_edge.side_effect = [mock_driver_instance1, mock_driver_instance2]
        
        manager = CWebDriver.get_instance()
        driver1 = manager.create_driver(enable_timeout=True)
        
        # 創建新Driver
        driver2 = manager.create_driver(enable_timeout=True)
        
        # 檢查舊Driver是否被關閉
        mock_driver_instance1.quit.assert_called_once()
