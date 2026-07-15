"""刪除訂票API"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.utils.response_helper import create_error_response, create_success_response
from src.utils.database import Database

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/delete-booking-ticket/<int:booking_id>', methods=['DELETE'])
def delete_booking_ticket(booking_id):
    """
    刪除訂票API
    
    URI: /delete-booking-ticket/{booking_id}
    """
    try:
        # 建立資料庫連線
        db = Database()
        db.connect()
        
        try:
            # 查詢訂票資訊
            sql = "SELECT TICKET_NUMBER, USER_ID, TICKET_TYPE FROM TB_BOOKING_THICKET WHERE BOOKING_ID = %s"
            booking = db.fetch_one(sql, (booking_id,))
            
            if not booking:
                return jsonify(create_error_response("訂票資訊不存在")), 404
            
            # 檢查是否已完成訂票
            if booking['TICKET_NUMBER']:
                return jsonify(create_error_response("該資料已完成訂票，無法進行刪除")), 400
            
            user_id = booking['USER_ID']
            ticket_type = booking['TICKET_TYPE']
            
            # 刪除早鳥票乘坐者
            delete_early_sql = "DELETE FROM TB_EARLY_BIRD WHERE BOOKING_ID = %s"
            db.execute(delete_early_sql, (booking_id,))
            
            # 刪除訂票資訊
            delete_booking_sql = "DELETE FROM TB_BOOKING_THICKET WHERE BOOKING_ID = %s"
            db.execute(delete_booking_sql, (booking_id,))
            
            # 查詢刪除後的訂票資訊
            system_date = datetime.now().date()
            next_day = (system_date + timedelta(days=1)).strftime('%Y-%m-%d')
            
            search_sql = """
            SELECT BOOKING_ID as id, BOOKING_DATE as booking_date, BOOKING_TIME as booking_time,
                   START_STATION as start_station, END_STATION as end_station, 
                   TICKET_NUMBER as ticket_number
            FROM TB_BOOKING_THICKET
            WHERE USER_ID = %s AND TICKET_TYPE = %s AND BOOKING_DATE >= %s
            ORDER BY BOOKING_DATE DESC
            """
            
            results = db.fetch_all(search_sql, (user_id, ticket_type, next_day))
            
            # 組織回應數據
            booking_info = []
            for row in results:
                booking_info.append({
                    'id': row['id'],
                    'booking_date': row['booking_date'].strftime('%Y-%m-%d'),
                    'booking_time': str(row['booking_time']),
                    'start_station': row['start_station'],
                    'end_station': row['end_station'],
                    'ticket_number': row['ticket_number'] or '',
                    'canDelete': not row['ticket_number']
                })
            
            response_info = {
                'ticket_type': ticket_type,
                'booking_info': booking_info
            }
            
            return jsonify(create_success_response('已成功刪除預約訂票資訊', response_info)), 200
        
        finally:
            db.disconnect()
    
    except Exception as e:
        return jsonify(create_error_response(f"伺服器錯誤: {str(e)}")), 500
