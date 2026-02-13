# Requirements.txt 维护指南

## ⚠️ 重要警告

**切勿使用 `pip freeze > requirements.txt`！**

这会将本地环境的所有包写入 requirements.txt，包括：
- `dbus-python` - 需要 dbus-1 系统库，Render 上没有
- `PyGObject` - 需要 GTK+ 系统库，Render 上没有
- `watchdog` - 会自动引入 dbus-python

这些包会导致编译失败！

## ✅ 正确做法

### 方案 1：使用 requirements_minimal.txt（推荐）

```bash
cp requirements_minimal.txt requirements.txt
```

### 方案 2：手动维护

直接编辑 `requirements.txt`，只添加需要的包。

```txt
# 示例
flask==3.1.2
gunicorn==23.0.0
```

### 方案 3：使用依赖分析工具

```bash
pip install pipdeptree
pipdeptree --packages flask > requirements.txt
```

## 🔍 Git Hook 保护

项目已安装 Git pre-commit hook，会自动检查 requirements.txt 是否包含问题包。

如果尝试提交包含 `dbus-python`、`PyGObject` 或 `watchdog` 的 requirements.txt，提交会被拒绝。

## 📦 最小化依赖列表

当前核心依赖（37 个包）：
- Coze SDK（4 个）
- LangGraph 和 LangChain（5 个）
- Flask 和 Gunicorn（3 个）
- 数据处理（3 个：numpy、pandas、pillow）
- HTTP 请求（4 个）
- 视频处理（1 个：opencv-python）
- 文件处理（2 个）
- 其他必要依赖（15 个）

## 🚫 禁用的脚本

- `scripts/pack.sh` - 已禁用，原脚本使用 `pip freeze`

## 💡 添加新依赖

1. 确定需要的包及其版本
2. 手动添加到 requirements.txt
3. 测试：在干净环境中安装并运行
4. 提交：`git add requirements.txt && git commit`

## 📋 常见问题

### Q: 为什么不用 `pip freeze`？

A: `pip freeze` 会列出所有包，包括系统依赖，导致编译失败。

### Q: 如何知道缺少哪些依赖？

A: 运行应用时，Python 会提示缺少的包，然后手动添加。

### Q: Render 编译失败怎么办？

A: 检查 requirements.txt 是否包含问题包，删除它们。
