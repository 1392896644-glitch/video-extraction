#!/bin/bash

echo "========================================="
echo "  🎬 视频文案提取系统 - 一键启动"
echo "========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3"
    echo "请先安装Python3"
    exit 1
fi

echo "✅ Python3已安装: $(python3 --version)"
echo ""

# 检查Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask未安装，正在安装..."
    pip3 install Flask Werkzeug
    echo "✅ Flask安装完成"
    echo ""
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p /tmp/uploads
mkdir -p templates
mkdir -p static/css
mkdir -p static/js

echo ""
echo "========================================="
echo "  🚀 启动服务中..."
echo "========================================="
echo ""
echo "📱 请在浏览器中打开："
echo "   http://localhost:5000"
echo ""
echo "💡 提示：按 Ctrl+C 可以停止服务"
echo ""
echo "========================================="
echo ""

# 启动Flask应用
cd /workspace/projects
python3 app.py
