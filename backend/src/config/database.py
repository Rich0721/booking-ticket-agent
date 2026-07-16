"""
資料庫連接配置

根據環境變數設定資料庫連接
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.objects.models.booking_ticket_models import Base


def get_db_url() -> str:
    """
    從環境變數取得資料庫URL
    
    Returns:
        str: 資料庫連接字符串
    """
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "root")
    db_name = os.getenv("DB_NAME", "booking_ticket")
    db_port = os.getenv("DB_PORT", "3306")
    
    # MySQL連接字符串格式: mysql+pymysql://user:password@host:port/database
    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_engine():
    """
    取得SQLAlchemy Engine
    
    Returns:
        Engine: SQLAlchemy Engine實例
    """
    db_url = get_db_url()
    return create_engine(
        db_url,
        echo=os.getenv("DEBUG", "False").lower() == "true",  # 調試模式下顯示SQL
        pool_pre_ping=True  # 測試連接是否仍然有效
    )


def get_session_factory():
    """
    取得Session工廠
    
    Returns:
        sessionmaker: SQLAlchemy sessionmaker實例
    """
    engine = get_engine()
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_db_session() -> Session:
    """
    取得資料庫Session
    
    Returns:
        Session: SQLAlchemy Session實例
    """
    SessionLocal = get_session_factory()
    return SessionLocal()


def init_db():
    """
    初始化資料庫，建立所有表
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
