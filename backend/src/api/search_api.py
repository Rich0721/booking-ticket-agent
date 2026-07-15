"""查詢訂票API"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.utils.validators import validate_tw_id
from src.utils.response_helper import create_error_response, create_success_response
from src.utils.database import Database

search_bp = Blueprint('search', __name__)

@search_bp.route('/search-booking-ticket', methods=['POST'])
def search_booking_ticket():
    """
    查詢訂票API
    
    Request body:
    {
        "info": {
            "user_id": "A123456789",
            "ticket_type": "THSR"
        }
    }
    """
    try:
        data = request.get_json()
        if not data or 'info' not in data:
            return jsonify(create_error_response("請求格式錯誤")), 400
        
        info = data['info']
        
        # 驗證必填欄位
        if 'user_id' not in info or 'ticket_type' not in info:
            return jsonify(create_error_response("缺少必填欄位")), 400
        
        user_id = info['user_id']
        ticket_type = info['ticket_type']
        
        # 驗證身份證
        if not validate_tw_id(user_id):
            return jsonify(create_error_response("身份證字號格式不正確")), 400
        
        # 建立資料庫連線
        db = Database()
        db.connect()
        
        try:
            # 查詢T+1開始的預約資訊
            system_date = datetime.now().date()
            next_day = (system_date + timedelta(days=1)).strftime('%Y-%m-%d')
            
            sql = """
            SELECT BOOKING_ID as id, BOOKING_DATE as booking_date, BOOKING_TIME as booking_time,
                   START_STATION as start_station, END_STATION as end_station, 
                   TICKET_NUMBER as ticket_number
            FROM TB_BOOKING_THICKET
            WHERE USER_ID = %s AND TICKET_TYPE = %s AND BOOKING_DATE >= %s
            ORDER BY BOOKING_DATE DESC
            """
            
            results = db.fetch_all(sql, (user_id, ticket_type, next_day))
            
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
            
            return jsonify(create_success_response('', response_info)), 200
        
        finally:
            db.disconnect()
    
    except Exception as e:
        return jsonify(create_error_response(f"伺服器錯誤: {str(e)}")), 500
