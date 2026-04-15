#!/bin/bash

# 考研英语辅助Agent启动脚本
# 用于Render部署

echo "正在启动考研英语辅助Agent..."

# 检查Python版本
python --version

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 安装前端依赖并构建
echo "构建前端..."
cd frontend
npm install
npm run build
cd ..

# 启动应用
echo "启动应用..."
gunicorn app.main:app \
  --config gunicorn_config.py \
  --bind 0.0.0.0:$PORT \
  --workers 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -

echo "应用已启动，监听端口: $PORT"