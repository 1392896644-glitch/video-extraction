# 🎬 视频文案提取系统

> 上传视频，自动提取文案、分析痛点、生成5种风格改写，保存到飞书表格

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

- 📹 **视频上传**：支持多种视频格式
- 🎯 **文案提取**：AI自动识别视频中的文字
- 📝 **文案摘要**：智能生成核心摘要
- 🔬 **深度分析**：分析痛点、人群画像、成功原因
- ✍️ **5种改写**：生成不同风格的改写文案
- 📊 **飞书集成**：自动保存到飞书多维表格

## 🚀 在线体验

**Demo地址**：[https://your-app.onrender.com](https://your-app.onrender.com)
（部署后替换为实际地址）

## 📦 本地运行

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/video-extraction.git
cd video-extraction
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
export PYTHONPATH=/path/to/project/src:$PYTHONPATH
python3 app.py
```

### 4. 访问应用

打开浏览器访问：`http://localhost:5000`

## 🌐 公网部署

### 方案1：Render（推荐）

1. Fork本项目到GitHub
2. 访问 [render.com](https://render.com)
3. 连接GitHub账号
4. 新建Web Service，选择本项目
5. 使用 `render.yaml` 配置
6. 点击部署，自动获得公网URL

### 方案2：Railway

1. 访问 [railway.app](https://railway.app)
2. 新建Project → Deploy from GitHub
3. 选择本项目
4. 使用 `railway.json` 配置
5. 部署完成，获得公网URL

### 方案3：云服务器

详见 [PUBLIC_DEPLOY_GUIDE.md](PUBLIC_DEPLOY_GUIDE.md)

## 📁 项目结构

```
.
├── app.py                    # Flask主应用
├── requirements.txt          # Python依赖
├── render.yaml              # Render配置
├── railway.json             # Railway配置
├── templates/
│   └── index.html          # 前端页面
├── src/
│   ├── graphs/             # 工作流定义
│   │   ├── graph.py
│   │   ├── state.py
│   │   └── nodes/
│   └── utils/              # 工具类
└── config/                # 配置文件
```

## 🔧 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| PYTHONPATH | Python路径 | /app/src |
| PORT | 服务端口 | 5000 |
| SECRET_KEY | Flask密钥 | 自动生成 |

## 📝 使用说明

### 上传视频
- 支持格式：MP4、MOV、AVI、FLV、WEBM、MKV
- 最大大小：500MB

### 查看结果
- 处理完成后显示飞书表格链接
- 点击链接查看完整的文案分析

## 🛠️ 技术栈

- **后端**：Python 3.12 + Flask + LangGraph
- **前端**：HTML5 + CSS3 + JavaScript
- **AI引擎**：豆包大模型（doubao）
- **存储**：飞书多维表格

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- Issue：[GitHub Issues](https://github.com/yourusername/video-extraction/issues)
- Email：your.email@example.com

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
