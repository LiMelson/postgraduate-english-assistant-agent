"""
WSGI入口点文件 - 用于Render部署
这个文件放在项目根目录，解决导入路径问题
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 现在可以正常导入
from app.main import app

# 这是WSGI应用对象
application = app

if __name__ == "__main__":
    # 本地开发时运行
    from config.settings import APP_CONFIG
    app.run(
        host=APP_CONFIG["host"],
        port=APP_CONFIG["port"],
        debug=APP_CONFIG["debug"]
    )