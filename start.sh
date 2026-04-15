#!/bin/bash

# 简单的启动脚本
echo "启动考研英语辅助Agent..."
gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120