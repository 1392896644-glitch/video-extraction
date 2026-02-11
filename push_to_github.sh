#!/bin/bash

echo "========================================="
echo "  📤 一键推送到GitHub"
echo "========================================="
echo ""

# 检查是否已初始化git
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
    echo ""
fi

# 读取GitHub仓库地址
echo "请输入你的GitHub仓库地址："
echo "例如：https://github.com/username/video-extraction.git"
read -p "> " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 仓库地址不能为空"
    exit 1
fi

echo ""
echo "📋 添加文件..."

# 添加所有文件
git add .

echo ""
echo "💬 请输入提交信息（留空使用默认）："
read -p "> " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="feat: 部署视频文案提取系统"
fi

echo ""
echo "📝 提交变更..."
git commit -m "$COMMIT_MSG"

echo ""
echo "🚀 推送到GitHub..."

# 添加远程仓库（如果还没添加）
if ! git remote get-url origin &> /dev/null; then
    git remote add origin $REPO_URL
else
    git remote set-url origin $REPO_URL
fi

# 推送到main分支
git push -u origin main || git push -u origin master

echo ""
echo "========================================="
echo "  ✅ 推送完成！"
echo "========================================="
echo ""
echo "📱 下一步："
echo "1. 访问你的GitHub仓库："
echo "   $REPO_URL"
echo ""
echo "2. 在Render或Railway部署："
echo "   Render: https://render.com"
echo "   Railway: https://railway.app"
echo ""
echo "3. 选择'Deploy from GitHub'"
echo "4. 选择这个仓库，点击部署"
echo ""
echo "5. 等待部署完成，获得公网URL！"
echo "========================================="
