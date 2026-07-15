"""後端主程式"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.api.booking_api import booking_bp
from src.api.search_api import search_bp
from src.api.delete_api import delete_bp
from src.api.menu_api import menu_bp

# 載入環境變數
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'env', '.env.dev'))

# 建立Flask應用
app = Flask(__name__)
CORS(app)

# 註冊API Blueprint
app.register_blueprint(booking_bp)
app.register_blueprint(search_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(menu_bp)

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
