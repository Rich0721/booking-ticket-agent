from datetime import date, time

from fastapi.testclient import TestClient
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.database.CTableBookingTicket import CTableBookingTicket


def test_reserve_invalid_id(client: TestClient, reserve_payload: dict) -> None:
    reserve_payload["info"]["user_id"] = "A123"
    response = client.post("/api/v1/booking/reserve", json=reserve_payload)

    assert response.status_code == 400
    assert response.json()["info"]["message"] == "訂票者ID輸入錯誤"


def test_reserve_early_bird_count_mismatch(client: TestClient, reserve_payload: dict) -> None:
    reserve_payload["info"]["early_ids"] = []
    response = client.post("/api/v1/booking/reserve", json=reserve_payload)

    assert response.status_code == 400
    assert response.json()["info"]["message"] == "全票與早鳥票數量需相同"


def test_reserve_reject_same_day(client: TestClient, reserve_payload: dict) -> None:
    reserve_payload["info"]["booking_date"] = date(2026, 7, 1).isoformat()
    response = client.post("/api/v1/booking/reserve", json=reserve_payload)

    assert response.status_code == 400
    assert response.json()["info"]["message"] == "當天不接受預約訂票"


def test_reserve_within_29_days(client: TestClient, reserve_payload: dict) -> None:
    reserve_payload["info"]["booking_date"] = date(2026, 7, 21).isoformat()
    response = client.post("/api/v1/booking/reserve", json=reserve_payload)

    assert response.status_code == 200
    assert response.json()["info"]["message"] == "2026/07/02將完成訂票，請記得查詢取票號碼"


def test_reserve_over_29_days_sunday_rule(client: TestClient, reserve_payload: dict) -> None:
    reserve_payload["info"]["booking_date"] = date(2026, 8, 2).isoformat()
    response = client.post("/api/v1/booking/reserve", json=reserve_payload)

    assert response.status_code == 200
    assert response.json()["info"]["message"] == "2026/07/03將完成訂票，請記得查詢取票號碼"


def test_search_returns_t_plus_one_records(client: TestClient, reserve_payload: dict) -> None:
    reserve_payload["info"]["booking_date"] = date(2026, 7, 21).isoformat()
    client.post("/api/v1/booking/reserve", json=reserve_payload)

    search_payload = {
        "headers": {"status_code": 0, "user_agent": "pytest"},
        "info": {"user_id": "A123456789", "ticket_type": "THSR"},
    }

    response = client.post("/api/v1/booking/search", json=search_payload)

    assert response.status_code == 200
    assert len(response.json()["info"]["booking_info"]) == 1


def test_delete_unprocessed_success(client: TestClient, reserve_payload: dict) -> None:
    reserve_response = client.post("/api/v1/booking/reserve", json=reserve_payload)
    booking_id = reserve_response.json()["info"]["booking_id"]

    delete_payload = {
        "headers": {"status_code": 0, "user_agent": "pytest"},
        "info": {"booking_id": booking_id, "user_id": "A123456789", "ticket_type": "THSR"},
    }

    response = client.post("/api/v1/booking/delete", json=delete_payload)

    assert response.status_code == 200
    assert response.json()["info"]["message"] == "刪除成功"


def test_delete_processed_record_rejected(
    client: TestClient,
    db_session: Session,
    reserve_payload: dict,
) -> None:
    reserve_response = client.post("/api/v1/booking/reserve", json=reserve_payload)
    booking_id = reserve_response.json()["info"]["booking_id"]

    db_session.execute(
        update(CTableBookingTicket)
        .where(CTableBookingTicket.booking_id == booking_id)
        .values(ticket_number="A12345")
    )
    db_session.commit()

    delete_payload = {
        "headers": {"status_code": 0, "user_agent": "pytest"},
        "info": {"booking_id": booking_id, "user_id": "A123456789", "ticket_type": "THSR"},
    }

    response = client.post("/api/v1/booking/delete", json=delete_payload)

    assert response.status_code == 400
    assert response.json()["info"]["message"] == "已完成訂票不可刪除"
