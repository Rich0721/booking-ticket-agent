"""資料庫連線相關工具函式"""
import os
import pymysql
from typing import Any, List, Tuple, Optional

class Database:
    """資料庫連線管理類別"""
    
    def __init__(self, host: str = None, user: str = None, password: str = None, database: str = None):
        """
        初始化資料庫連線
        
        Args:
            host: 資料庫主機
            user: 資料庫使用者
            password: 資料庫密碼
            database: 資料庫名稱
        """
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.database = database or os.getenv('DB_NAME', 'booking_ticket')
        self.connection = None
    
    def connect(self):
        """建立資料庫連線"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.Error as e:
            raise Exception(f"資料庫連線失敗: {e}")
    
    def disconnect(self):
        """關閉資料庫連線"""
        if self.connection:
            self.connection.close()
    
    def execute(self, sql: str, args: tuple = ()) -> int:
        """
        執行INSERT/UPDATE/DELETE操作
        
        Args:
            sql: SQL語句
            args: SQL參數
            
        Returns:
            int: 受影響的行數
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, args)
                self.connection.commit()
                return cursor.rowcount
        except pymysql.Error as e:
            self.connection.rollback()
            raise Exception(f"SQL執行失敗: {e}")
    
    def fetch_one(self, sql: str, args: tuple = ()) -> Optional[dict]:
        """
        查詢單一記錄
        
        Args:
            sql: SQL語句
            args: SQL參數
            
        Returns:
            dict: 查詢結果
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, args)
                return cursor.fetchone()
        except pymysql.Error as e:
            raise Exception(f"SQL查詢失敗: {e}")
    
    def fetch_all(self, sql: str, args: tuple = ()) -> List[dict]:
        """
        查詢所有記錄
        
        Args:
            sql: SQL語句
            args: SQL參數
            
        Returns:
            list: 查詢結果列表
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, args)
                return cursor.fetchall()
        except pymysql.Error as e:
            raise Exception(f"SQL查詢失敗: {e}")
