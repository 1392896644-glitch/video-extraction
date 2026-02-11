#!/bin/bash

echo "========================================="
echo "  🌐 公网部署脚本 - 让全世界都能访问"
echo "========================================="
echo ""

# 检查环境
echo "📋 环境检查..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安装Python3"
    exit 1
fi

echo "✅ Python3版本: $(python3 --version)"
echo ""

# 安装依赖
echo "📦 安装依赖..."
pip3 install Flask Werkzeug gunicorn -q
echo "✅ 依赖安装完成"
echo ""

# 创建必要目录
mkdir -p /tmp/uploads

# 设置环境变量
export PYTHONPATH=/workspace/projects/src:$PYTHONPATH
export FLASK_APP=app.py
export FLASK_ENV=production

echo "========================================="
echo "  🚀 启动公网服务..."
echo "========================================="
echo ""
echo "📱 本地访问: http://localhost:5000"
echo "🌐 公网访问: 需要配置域名或使用内网穿透"
echo ""
echo "📋 部署方式："
echo "1. 云服务器部署（推荐）"
echo "2. 内网穿透（临时）"
echo "3. 云平台托管（Render/Railway）"
echo ""
echo "========================================="
echo ""

# 使用Gunicorn启动（生产环境）
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - --log-level info app:app
