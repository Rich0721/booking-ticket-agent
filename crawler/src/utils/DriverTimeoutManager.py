import threading
import time
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)


class DriverTimeoutManager:
    """
    Driver超時管理器，用於監控和處理Driver卡住的情況
    """
    
    def __init__(self, timeout_seconds: float = 60.0):
        """
        初始化超時管理器
        
        Args:
            timeout_seconds: 超時時間（秒）
        """
        self.timeout_seconds = timeout_seconds
        self._watchdog_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._last_activity_time = time.time()
        self._timeout_callback: Optional[Callable] = None
        self._lock = threading.Lock()
        self._timed_out = False  # 超時狀態標誌
    
    def set_timeout_callback(self, callback: Callable) -> None:
        """
        設置超時回調函數
        
        Args:
            callback: 超時時調用的回調函數
        """
        self._timeout_callback = callback
    
    def start(self) -> None:
        """啟動超時監控"""
        with self._lock:
            if self._is_running:
                return
            
            self._is_running = True
            self._timed_out = False
            self._last_activity_time = time.time()
        
        self._watchdog_thread = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._watchdog_thread.start()
        logger.debug(f"超時監控已啟動 (超時時間: {self.timeout_seconds}秒)")
    
    def stop(self) -> None:
        """停止超時監控"""
        with self._lock:
            self._is_running = False
        
        if self._watchdog_thread:
            self._watchdog_thread.join(timeout=2)
        logger.debug("超時監控已停止")
    
    def reset_activity(self) -> None:
        """重置活動時間戳（表示有新的活動）"""
        with self._lock:
            self._last_activity_time = time.time()
            self._timed_out = False
    
    def _watchdog_loop(self) -> None:
        """監控線程的主循環"""
        while True:
            try:
                with self._lock:
                    if not self._is_running:
                        break
                    
                    elapsed_time = time.time() - self._last_activity_time
                    
                    if elapsed_time > self.timeout_seconds and not self._timed_out:
                        logger.warning(
                            f"Driver超時 (已卡住 {elapsed_time:.1f}秒，超時時間: {self.timeout_seconds}秒)"
                        )
                        self._timed_out = True
                        
                        # 執行回調
                        if self._timeout_callback:
                            try:
                                self._timeout_callback()
                            except Exception as e:
                                logger.error(f"超時回調執行失敗: {str(e)}")
                
                # 檢查間隔為1秒
                time.sleep(1)
            
            except Exception as e:
                logger.error(f"監控線程異常: {str(e)}")
                break
    
    def is_timeout(self) -> bool:
        """檢查是否已超時"""
        with self._lock:
            return self._timed_out
