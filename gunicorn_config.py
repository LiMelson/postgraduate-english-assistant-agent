import os

# Gunicorn 配置文件
workers = int(os.environ.get('GUNICORN_WORKERS', '4'))
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', '5'))
worker_class = 'sync'
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
accesslog = '-'  # 输出到 stdout
errorlog = '-'   # 输出到 stderr