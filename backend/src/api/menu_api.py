"""載入選單API"""
from flask import Blueprint, request, jsonify
from src.utils.response_helper import create_error_response, create_success_response
from src.utils.database import Database

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/loading-selected', methods=['GET'])
def loading_selected():
    """
    載入選單API
    
    Query: ?parm_category={parm_category}
    """
    try:
        parm_category = request.args.get('parm_category')
        
        if not parm_category:
            return jsonify(create_error_response("缺少parm_category參數")), 400
        
        # 建立資料庫連線
        db = Database()
        db.connect()
        
        try:
            # 查詢選單資料
            sql = """
            SELECT PARM_ID as id, PARM_NAME as parm_name, PARM_VALUE as parm_value
            FROM TB_SYS_PARM
            WHERE PARM_CATEGORY = %s
            ORDER BY PARM_ID
            """
            
            results = db.fetch_all(sql, (parm_category,))
            
            # 組織回應數據
            menu = []
            for row in results:
                menu.append({
                    'id': row['id'],
                    'parm_name': row['parm_name'],
                    'parm_value': row['parm_value']
                })
            
            response_info = {
                'menu': menu
            }
            
            return jsonify(create_success_response('', response_info)), 200
        
        finally:
            db.disconnect()
    
    except Exception as e:
        return jsonify(create_error_response(f"伺服器錯誤: {str(e)}")), 500
