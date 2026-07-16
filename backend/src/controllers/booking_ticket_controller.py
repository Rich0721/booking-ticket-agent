from fastapi import APIRouter, HTTPException
from datetime import datetime
from src.utils.models import BookingTicketRequest, BookingTicketResponse
from src.objects.classes.CBookingTicketInfo import CBookingTicketInfo
from src.services.BookingTicketService import BookingTicketService
from src.repositories.BookingTicketRepository import BookingTicketRepository


router = APIRouter()


@router.post("/booking-ticket")
async def booking_ticket(request: BookingTicketRequest) -> dict:
    """
    預約訂票API
    
    Args:
        request: 預約訂票請求資訊
        
    Returns:
        預約訂票結果
    """
    try:
        # 將request轉換為CBookingTicketInfo物件
        booking_date = datetime.strptime(request.booking_date, "%Y-%m-%d").date()
        
        booking_info = CBookingTicketInfo(
            user_id=request.user_id,
            ticket_type=request.ticket_type,
            booking_date=booking_date,
            booking_time=request.booking_time,
            start_station=request.start_station,
            end_station=request.end_station,
            adults=request.adults,
            childs=request.childs,
            students=request.students,
            elders=request.elders,
            disables=request.disables,
            is_early_bird=request.is_early_bird,
            is_member=request.is_member,
            early_ids=request.early_ids
        )
        
        # 建立服務層實例
        # TODO: 從dependency injection獲取repository
        repository = BookingTicketRepository(None)
        service = BookingTicketService(repository)
        
        # 處理預約訂票
        system_date = datetime.now()
        success, message = service.process_booking(booking_info, system_date)
        
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        return {
            "headers": {
                "message": message
            }
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
