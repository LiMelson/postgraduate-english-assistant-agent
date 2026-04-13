import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS
from app.api.routes import api_bp
from config.settings import APP_CONFIG

app = Flask(__name__)

# 启用CORS
CORS(app)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(
        host=APP_CONFIG["host"],
        port=APP_CONFIG["port"],
        debug=APP_CONFIG["debug"]
    )
