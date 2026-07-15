"""預約訂票API"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from src.utils.validators import validate_tw_id, validate_date_format, validate_time_format
from src.utils.date_helper import calculate_booking_completion_date, get_message_for_booking_date, parse_date_string
from src.utils.response_helper import create_error_response, create_success_response
from src.utils.database import Database

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking-ticket', methods=['POST'])
def booking_ticket():
    """
    預約訂票API
    
    Request body:
    {
        "info": {
            "user_id": "A123456789",
            "ticket_type": "THSR",
            "booking_date": "2026-07-03",
            "booking_time": "10:30",
            "start_station": "台北",
            "end_station": "左營",
            "adults": 1,
            "childs": 0,
            "students": 0,
            "elders": 0,
            "disables": 0,
            "is_early_bird": true,
            "is_member": true,
            "early_ids": ["A123456789", "B123456789"]
        }
    }
    """
    try:
        data = request.get_json()
        if not data or 'info' not in data:
            return jsonify(create_error_response("請求格式錯誤")), 400
        
        info = data['info']
        
        # 驗證必填欄位
        required_fields = ['user_id', 'ticket_type', 'booking_date', 'booking_time', 
                          'start_station', 'end_station', 'adults']
        for field in required_fields:
            if field not in info:
                return jsonify(create_error_response(f"缺少必填欄位: {field}")), 400
        
        # 驗證身份證
        user_id = info['user_id']
        if not validate_tw_id(user_id):
            return jsonify(create_error_response("身份證字號格式不正確")), 400
        
        # 驗證日期格式
        booking_date_str = info['booking_date']
        if not validate_date_format(booking_date_str):
            return jsonify(create_error_response("日期格式不正確，應為YYYY-MM-DD")), 400
        
        # 驗證時間格式
        booking_time_str = info['booking_time']
        if not validate_time_format(booking_time_str):
            return jsonify(create_error_response("時間格式不正確，應為HH:MM")), 400
        
        # 驗證早鳥票ID數量
        adults = info.get('adults', 0)
        early_ids = info.get('early_ids', [])
        if info.get('is_early_bird', False) and len(early_ids) != adults:
            return jsonify(create_error_response("早鳥票ID數量須與全票(Adults)相同")), 400
        
        # 驗證早鳥票ID格式
        for early_id in early_ids:
            if not validate_tw_id(early_id):
                return jsonify(create_error_response(f"早鳥票ID格式不正確: {early_id}")), 400
        
        # 計算訂票完成日期
        # 允許從header注入系統日期用於測試
        system_date_str = request.headers.get('X-System-Date')
        if system_date_str:
            system_date = parse_date_string(system_date_str)
        else:
            system_date = datetime.now()
        
        departure_date = parse_date_string(booking_date_str)
        
        try:
            completion_date = calculate_booking_completion_date(system_date, departure_date)
        except ValueError as e:
            return jsonify(create_error_response(str(e))), 400
        
        # 建立資料庫連線
        db = Database()
        db.connect()
        
        try:
            # 新增預約訂票資訊
            sql = """
            INSERT INTO TB_BOOKING_THICKET 
            (USER_ID, ADULT_COUNT, CHILD_COUNT, STUDENT_COUNT, ELDER_COUNT, DISABLED_COUNT, 
             TICKET_TYPE, TICKET_NUMBER, BOOKING_DATE, BOOKING_TIME, START_STATION, END_STATION,
             IS_EARLY_BIRD, IS_MEMBER, CAN_BOOK_DATE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            args = (
                user_id,
                info.get('adults', 0),
                info.get('childs', 0),
                info.get('students', 0),
                info.get('elders', 0),
                info.get('disables', 0),
                info['ticket_type'],
                '',  # 初始為空
                booking_date_str,
                booking_time_str,
                info['start_station'],
                info['end_station'],
                1 if info.get('is_early_bird', False) else 0,
                1 if info.get('is_member', False) else 0,
                completion_date.strftime('%Y-%m-%d')
            )
            
            db.execute(sql, args)
            
            # 取得新增的訂票ID
            last_id_result = db.fetch_one("SELECT LAST_INSERT_ID() as id")
            booking_id = last_id_result['id']
            
            # 新增早鳥票乘坐者
            if early_ids:
                for early_id in early_ids:
                    sql = """
                    INSERT INTO TB_EARLY_BIRD (BOOKING_ID, USER_ID)
                    VALUES (%s, %s)
                    """
                    db.execute(sql, (booking_id, early_id))
            
            message = get_message_for_booking_date(completion_date)
            return jsonify(create_success_response(message)), 200
        
        finally:
            db.disconnect()
    
    except Exception as e:
        return jsonify(create_error_response(f"伺服器錯誤: {str(e)}")), 500
