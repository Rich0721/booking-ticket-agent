from selenium import webdriver
from selenium.webdriver.edge.service import Service
from typing import Optional


class CWebDriver:
    """WebDriver管理類，處理Edge瀏覽器實例"""
    
    __instance: Optional['CWebDriver'] = None
    __driver: Optional[webdriver.Edge] = None
    
    def __init__(self):
        if CWebDriver.__instance is not None:
            raise Exception("CWebDriver is a singleton class")
        self.__driver = None
    
    @staticmethod
    def get_instance() -> 'CWebDriver':
        if CWebDriver.__instance is None:
            CWebDriver.__instance = CWebDriver.__new__(CWebDriver)
            CWebDriver.__instance.__driver = None
        return CWebDriver.__instance
    
    def create_driver(self) -> webdriver.Edge:
        """建立Edge WebDriver實例"""
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Edge(options=options)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => false})'
        })
        
        self.__driver = driver
        return driver
    
    def get_driver(self) -> Optional[webdriver.Edge]:
        """取得當前的WebDriver實例"""
        return self.__driver
    
    def close_driver(self) -> None:
        """關閉WebDriver實例"""
        if self.__driver:
            self.__driver.quit()
            self.__driver = None
