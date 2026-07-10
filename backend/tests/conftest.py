from datetime import date, time
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DB_DRIVER"] = "sqlite"
os.environ["DB_SQLITE_PATH"] = "./test_bootstrap.db"

from src.core import time_provider
from src.database.CBase import CBase
from src.database.CDatabase import get_db
from src.database import init_models  # noqa: F401
from src.main import app


@pytest.fixture(name="fixed_today")
def fixture_fixed_today(monkeypatch) -> date:
    mock_date = date(2026, 7, 1)
    monkeypatch.setattr(time_provider, "get_system_date", lambda: mock_date)
    return mock_date


@pytest.fixture(name="testing_session_local")
def fixture_testing_session_local():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
    CBase.metadata.create_all(bind=engine)

    try:
        yield testing_session_local
    finally:
        CBase.metadata.drop_all(bind=engine)


@pytest.fixture(name="db_session")
def fixture_db_session(testing_session_local) -> Session:
    session: Session = testing_session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client")
def fixture_client(testing_session_local, fixed_today: date) -> TestClient:
    def override_get_db():
        session: Session = testing_session_local()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(name="reserve_payload")
def fixture_reserve_payload() -> dict:
    return {
        "headers": {"status_code": 0, "user_agent": "pytest"},
        "info": {
            "user_id": "A123456789",
            "ticket_type": "THSR",
            "booking_date": date(2026, 7, 21).isoformat(),
            "booking_time": time(10, 30).isoformat(),
            "start_station": "台北",
            "end_station": "左營",
            "adults": 1,
            "childs": 0,
            "students": 0,
            "elders": 0,
            "disables": 0,
            "is_early_bird": True,
            "is_member": True,
            "early_ids": ["A123456789"],
        },
    }
