from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.core import time_provider
from src.database.CDatabase import get_db
from src.database.CTableBookingTicket import CTableBookingTicket
from src.database.CTableEarlyBird import CTableEarlyBird
from src.objects.classes.CBookingRequest import CBookingRequest
from src.objects.classes.CDeleteBookingRequest import CDeleteBookingRequest
from src.objects.classes.CSearchBookingRequest import CSearchBookingRequest
from src.utils.booking_rules import calculate_can_book_date, get_total_ticket_count
from src.utils.id_validator import is_valid_taiwan_id


router = APIRouter(prefix="/booking", tags=["booking"])


@router.post("/reserve")
def reserve_ticket(request_data: CBookingRequest, db: Session = Depends(get_db)) -> dict:
    system_date = time_provider.get_system_date()
    info = request_data.info

    if not is_valid_taiwan_id(info.user_id):
        raise HTTPException(status_code=400, detail="訂票者ID輸入錯誤")

    for early_id in info.early_ids:
        if not is_valid_taiwan_id(early_id):
            raise HTTPException(status_code=400, detail="早鳥票ID輸入錯誤")

    ticket_count = get_total_ticket_count(info.adults, info.childs, info.students, info.elders, info.disables)
    if ticket_count > 10:
        raise HTTPException(status_code=400, detail="訂購數量不可以超過10張")

    if info.is_early_bird and len(info.early_ids) != info.adults:
        raise HTTPException(status_code=400, detail="全票與早鳥票數量需相同")

    if info.booking_date <= system_date:
        raise HTTPException(status_code=400, detail="當天不接受預約訂票")

    can_book_date = calculate_can_book_date(system_date, info.booking_date)

    booking_record = CTableBookingTicket(
        user_id=info.user_id,
        adult_count=info.adults,
        child_count=info.childs,
        student_count=info.students,
        elder_count=info.elders,
        disabled_count=info.disables,
        ticket_type=info.ticket_type,
        ticket_number="",
        booking_date=info.booking_date,
        booking_time=info.booking_time,
        start_station=info.start_station,
        end_station=info.end_station,
        is_early_bird=info.is_early_bird,
        is_member=info.is_member,
        can_book_date=can_book_date,
    )
    db.add(booking_record)
    db.flush()

    if info.is_early_bird:
        db.add_all([CTableEarlyBird(booking_id=booking_record.booking_id, user_id=early_id) for early_id in info.early_ids])

    db.commit()

    return {
        "info": {
            "message": f"{can_book_date.strftime('%Y/%m/%d')}將完成訂票，請記得查詢取票號碼",
            "booking_id": booking_record.booking_id,
        }
    }


@router.post("/search")
def search_booking(request_data: CSearchBookingRequest, db: Session = Depends(get_db)) -> dict:
    system_date = time_provider.get_system_date()
    info = request_data.info

    if not is_valid_taiwan_id(info.user_id):
        raise HTTPException(status_code=400, detail="訂票者ID輸入錯誤")

    query = (
        select(CTableBookingTicket)
        .where(CTableBookingTicket.user_id == info.user_id)
        .where(CTableBookingTicket.ticket_type == info.ticket_type)
        .where(CTableBookingTicket.booking_date >= (system_date + timedelta(days=1)))
        .order_by(CTableBookingTicket.booking_date.asc(), CTableBookingTicket.booking_time.asc())
    )
    records = db.scalars(query).all()

    booking_info = [
        {
            "id": record.booking_id,
            "booking_date": record.booking_date.isoformat(),
            "booking_time": record.booking_time.strftime("%H:%M"),
            "start_station": record.start_station,
            "end_station": record.end_station,
            "ticket_number": record.ticket_number,
        }
        for record in records
    ]

    return {"info": {"ticket_type": info.ticket_type, "booking_info": booking_info}}


@router.post("/delete")
def delete_booking(request_data: CDeleteBookingRequest, db: Session = Depends(get_db)) -> dict:
    info = request_data.info

    if not is_valid_taiwan_id(info.user_id):
        raise HTTPException(status_code=400, detail="訂票者ID輸入錯誤")

    target = db.scalar(
        select(CTableBookingTicket)
        .where(CTableBookingTicket.booking_id == info.booking_id)
        .where(CTableBookingTicket.user_id == info.user_id)
        .where(CTableBookingTicket.ticket_type == info.ticket_type)
    )

    if target is None:
        raise HTTPException(status_code=404, detail="查無可刪除資料")

    if target.ticket_number:
        raise HTTPException(status_code=400, detail="已完成訂票不可刪除")

    db.execute(delete(CTableEarlyBird).where(CTableEarlyBird.booking_id == info.booking_id))
    db.delete(target)
    db.commit()

    return {"info": {"message": "刪除成功"}}
