#!/bin/bash
set -e

echo "开始安装依赖..."

# 清理缓存
pip cache purge

# 使用约束文件安装
pip install -r requirements.txt --constraint constraints.txt

echo "依赖安装完成！"
