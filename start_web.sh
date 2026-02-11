#!/bin/bash

# 启动Web应用的脚本

echo "🚀 启动视频文案提取与分析系统..."
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查并安装依赖
echo "📦 检查依赖..."
pip3 install -r requirements.txt

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p /tmp/uploads
mkdir -p templates
mkdir -p static/css
mkdir -p static/js

# 启动Flask应用
echo ""
echo "✅ 启动成功！"
echo "🌐 访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
