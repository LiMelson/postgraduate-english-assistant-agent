import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, send_from_directory
from flask_cors import CORS
from app.api.routes import api_bp
from config.settings import APP_CONFIG

app = Flask(__name__)

# 启用CORS
CORS(app)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 静态文件目录配置
FRONTEND_BUILD_DIR = os.path.join(project_root, 'frontend', 'dist')

# 确保目录存在
if not os.path.exists(FRONTEND_BUILD_DIR):
    os.makedirs(FRONTEND_BUILD_DIR, exist_ok=True)

# 提供静态文件服务
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_BUILD_DIR, path)):
        return send_from_directory(FRONTEND_BUILD_DIR, path)
    else:
        return send_from_directory(FRONTEND_BUILD_DIR, 'index.html')

if __name__ == '__main__':
    app.run(
        host=APP_CONFIG["host"],
        port=APP_CONFIG["port"],
        debug=APP_CONFIG["debug"]
    )