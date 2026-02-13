#!/bin/bash

# 注意：不要使用 pip freeze，会引入本地环境的所有包
# 使用 requirements_minimal.txt 替代

echo "⚠️  警告：此脚本已被禁用！"
echo "❌ pip freeze 会引入 dbus-python、PyGObject 等问题包"
echo "✅ 请使用 requirements_minimal.txt 或手动维护 requirements.txt"

# 禁用此脚本
# pip freeze > requirements.txt
