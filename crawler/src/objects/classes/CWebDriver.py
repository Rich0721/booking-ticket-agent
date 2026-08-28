from selenium import webdriver
from selenium.webdriver.edge.service import Service
from typing import Optional
from src.utils.DriverTimeoutManager import DriverTimeoutManager
import logging

logger = logging.getLogger(__name__)


class CWebDriver:
    """WebDriver管理類，處理Edge瀏覽器實例"""
    
    __instance: Optional['CWebDriver'] = None
    __driver: Optional[webdriver.Edge] = None
    
    # Driver超時時間設定（秒）
    DEFAULT_DRIVER_TIMEOUT = 30.0
    
    def __init__(self):
        if CWebDriver.__instance is not None:
            raise Exception("CWebDriver is a singleton class")
        self.__driver = None
        self.__timeout_manager: Optional[DriverTimeoutManager] = None
    
    @staticmethod
    def get_instance() -> 'CWebDriver':
        if CWebDriver.__instance is None:
            CWebDriver.__instance = CWebDriver.__new__(CWebDriver)
            CWebDriver.__instance.__driver = None
            CWebDriver.__instance.__timeout_manager = None
        return CWebDriver.__instance
    
    def create_driver(self, enable_timeout: bool = True) -> webdriver.Edge:
        """
        建立Edge WebDriver實例
        
        Args:
            enable_timeout: 是否啟用超時監控
        """
        # 關閉之前的driver和timeout manager
        self.close_driver()
        
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Edge(options=options)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => false})'
        })
        
        self.__driver = driver
        
        # 如果啟用超時監控，則建立超時管理器
        if enable_timeout:
            self.__timeout_manager = DriverTimeoutManager(
                timeout_seconds=self.DEFAULT_DRIVER_TIMEOUT
            )
            self.__timeout_manager.start()
        
        return driver
    
    def get_driver(self) -> Optional[webdriver.Edge]:
        """取得當前的WebDriver實例"""
        return self.__driver
    
    def reset_activity(self) -> None:
        """重置活動時間戳（表示Driver有響應）"""
        if self.__timeout_manager:
            self.__timeout_manager.reset_activity()
    
    def is_driver_timeout(self) -> bool:
        """檢查Driver是否已超時"""
        if self.__timeout_manager:
            return self.__timeout_manager.is_timeout()
        return False
    
    def close_driver(self) -> None:
        """關閉WebDriver實例"""
        # 先停止超時監控
        if self.__timeout_manager:
            self.__timeout_manager.stop()
            self.__timeout_manager = None
        
        # 然後關閉driver
        if self.__driver:
            try:
                self.__driver.quit()
            except Exception as e:
                logger.warning(f"關閉WebDriver時發生異常: {str(e)}")
            finally:
                self.__driver = None
