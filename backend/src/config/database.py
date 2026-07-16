"""
資料庫連接配置 - 抽象層設計

支持多種資料庫，通過環境變數切換，不需要修改應用代碼
當前支持: PostgreSQL (主要), MySQL (備用)
"""

import os
from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from src.objects.models.booking_ticket_models import Base


class DatabaseConfig:
    """
    資料庫通用配置
    """
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")  # PostgreSQL預設埠
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "postgres")
        self.database = os.getenv("DB_NAME", "booking_ticket")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.db_type = os.getenv("DB_TYPE", "postgresql").lower()  # 資料庫類型


class DatabaseProvider(ABC):
    """
    資料庫提供者抽象基類
    
    定義所有資料庫提供者必須實現的接口，允許未來輕鬆擴展其他資料庫
    """
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
    
    @abstractmethod
    def get_connection_string(self) -> str:
        """
        取得資料庫連接字符串
        
        Returns:
            str: 資料庫URL
        """
        pass
    
    @abstractmethod
    def get_engine(self) -> Engine:
        """
        取得SQLAlchemy Engine
        
        Returns:
            Engine: SQLAlchemy Engine實例
        """
        pass
    
    @abstractmethod
    def get_session_factory(self) -> sessionmaker:
        """
        取得Session工廠
        
        Returns:
            sessionmaker: SQLAlchemy sessionmaker實例
        """
        pass
    
    def get_db_session(self) -> Session:
        """
        取得資料庫Session
        
        Returns:
            Session: SQLAlchemy Session實例
        """
        if self._session_factory is None:
            self._session_factory = self.get_session_factory()
        return self._session_factory()
    
    def init_db(self):
        """
        初始化資料庫，建立所有表
        """
        engine = self.get_engine()
        Base.metadata.create_all(bind=engine)
    
    def get_engine_instance(self) -> Engine:
        """
        取得Engine實例（使用緩存）
        
        Returns:
            Engine: SQLAlchemy Engine實例
        """
        if self._engine is None:
            self._engine = self.get_engine()
        return self._engine


class PostgreSQLProvider(DatabaseProvider):
    """
    PostgreSQL資料庫提供者實現
    
    使用psycopg2驅動與PostgreSQL通信
    """
    
    def get_connection_string(self) -> str:
        """
        生成PostgreSQL連接字符串
        
        格式: postgresql+psycopg2://user:password@host:port/database
        """
        return (
            f"postgresql+psycopg2://{self.config.user}:{self.config.password}"
            f"@{self.config.host}:{self.config.port}/{self.config.database}"
        )
    
    def get_engine(self) -> Engine:
        """
        建立PostgreSQL Engine
        
        Returns:
            Engine: SQLAlchemy Engine實例，配置適合PostgreSQL的選項
        """
        return create_engine(
            self.get_connection_string(),
            echo=self.config.debug,
            pool_pre_ping=True,  # 測試連接是否仍然有效
            pool_size=10,  # 連接池大小
            max_overflow=20,  # 超過pool_size時最多允許的連接數
        )
    
    def get_session_factory(self) -> sessionmaker:
        """
        建立PostgreSQL Session工廠
        
        Returns:
            sessionmaker: PostgreSQL的sessionmaker實例
        """
        engine = self.get_engine_instance()
        return sessionmaker(bind=engine, expire_on_commit=False)


class MySQLProvider(DatabaseProvider):
    """
    MySQL資料庫提供者實現（備用）
    
    使用pymysql驅動與MySQL通信
    """
    
    def get_connection_string(self) -> str:
        """
        生成MySQL連接字符串
        
        格式: mysql+pymysql://user:password@host:port/database
        """
        return (
            f"mysql+pymysql://{self.config.user}:{self.config.password}"
            f"@{self.config.host}:{self.config.port}/{self.config.database}"
        )
    
    def get_engine(self) -> Engine:
        """
        建立MySQL Engine
        
        Returns:
            Engine: SQLAlchemy Engine實例，配置適合MySQL的選項
        """
        return create_engine(
            self.get_connection_string(),
            echo=self.config.debug,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
    
    def get_session_factory(self) -> sessionmaker:
        """
        建立MySQL Session工廠
        
        Returns:
            sessionmaker: MySQL的sessionmaker實例
        """
        engine = self.get_engine_instance()
        return sessionmaker(bind=engine, expire_on_commit=False)


class DatabaseFactory:
    """
    資料庫工廠類
    
    根據環境變數動態選擇資料庫提供者，支持輕鬆擴展新的資料庫
    """
    
    _providers = {
        "postgresql": PostgreSQLProvider,
        "postgres": PostgreSQLProvider,  # 別名
        "mysql": MySQLProvider,
    }
    
    @classmethod
    def create_provider(cls, config: Optional[DatabaseConfig] = None) -> DatabaseProvider:
        """
        創建資料庫提供者
        
        Args:
            config: 資料庫配置，若為None則使用環境變數
            
        Returns:
            DatabaseProvider: 資料庫提供者實例
            
        Raises:
            ValueError: 不支持的資料庫類型
        """
        if config is None:
            config = DatabaseConfig()
        
        provider_class = cls._providers.get(config.db_type)
        if provider_class is None:
            raise ValueError(
                f"Unsupported database type: {config.db_type}. "
                f"Supported types: {', '.join(cls._providers.keys())}"
            )
        
        return provider_class(config)
    
    @classmethod
    def register_provider(cls, db_type: str, provider_class: type):
        """
        註冊新的資料庫提供者
        
        用於支持新的資料庫類型，例如: DatabaseFactory.register_provider('oracle', OracleProvider)
        
        Args:
            db_type: 資料庫類型標識
            provider_class: 資料庫提供者類（必須繼承DatabaseProvider）
        """
        if not issubclass(provider_class, DatabaseProvider):
            raise TypeError(f"{provider_class} must inherit from DatabaseProvider")
        cls._providers[db_type] = provider_class


# ============================================================================
# 全局實例和便利函數（保持向後兼容性）
# ============================================================================

_global_provider: Optional[DatabaseProvider] = None


def get_provider() -> DatabaseProvider:
    """
    取得全局資料庫提供者實例
    
    Returns:
        DatabaseProvider: 資料庫提供者實例
    """
    global _global_provider
    if _global_provider is None:
        _global_provider = DatabaseFactory.create_provider()
    return _global_provider


def get_db_url() -> str:
    """
    取得資料庫連接URL
    
    Returns:
        str: 資料庫連接字符串
    """
    return get_provider().get_connection_string()


def get_engine() -> Engine:
    """
    取得SQLAlchemy Engine
    
    Returns:
        Engine: SQLAlchemy Engine實例
    """
    return get_provider().get_engine_instance()


def get_session_factory() -> sessionmaker:
    """
    取得Session工廠
    
    Returns:
        sessionmaker: SQLAlchemy sessionmaker實例
    """
    return get_provider()._session_factory or get_provider().get_session_factory()


def get_db_session() -> Session:
    """
    取得資料庫Session - FastAPI依賴注入函數
    
    Returns:
        Session: SQLAlchemy Session實例
    """
    return get_provider().get_db_session()


def init_db():
    """
    初始化資料庫，建立所有表
    """
    get_provider().init_db()
