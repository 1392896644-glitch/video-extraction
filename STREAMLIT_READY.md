# ✅ 已为你创建 Streamlit Cloud 版本！

## 🎉 新版本特点

**与 Render 版本完全相同的功能，但：**
- ✅ **部署超级简单**（1 分钟）
- ✅ **完全免费**
- ✅ **没有 dbus-python 问题**
- ✅ **内存充足**（1GB+）
- ✅ **专为 AI 应用设计**

---

## 🚀 立即部署（3 步）

### 第 1 步：访问 Streamlit Cloud
打开浏览器，访问：https://streamlit.io/cloud

### 第 2 步：登录并授权
1. 点击 "Sign in with GitHub"
2. 授权 GitHub 访问

### 第 3 步：创建应用
1. 点击 "New app"
2. 选择你的 GitHub 仓库
3. 配置如下：
   ```
   Repository: 1392896644-glitch/video-extraction
   Branch: main
   Main file path: app_streamlit.py
   Python version: 3.12
   Dependencies: requirements_streamlit.txt
   ```
4. 点击 "Deploy"

**等待 1-2 分钟，应用就部署成功了！** 🎉

---

## ⚙️ 配置环境变量

部署后，点击 "Settings" → "Secrets"，添加以下变量：

```
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_WORKLOAD_IDENTITY_CLIENT_ID=your_client_id
COZE_WORKLOAD_IDENTITY_CLIENT_SECRET=your_client_secret
COZE_BUCKET_ENDPOINT_URL=your_bucket_url
COZE_BUCKET_NAME=your_bucket_name
```

**这些值在哪里？**
- 访问 Coze 平台
- 进入你的项目设置
- 找到 "集成" → "工作负载身份"
- 复制这些值

---

## 📝 使用说明

1. 打开应用 URL（Streamlit 会提供）
2. 上传视频文件（mp4, mov, avi, flv, webm, mkv）
3. 点击 "开始处理" 按钮
4. 等待 1-2 分钟
5. 查看结果：
   - 提取的文案
   - 文案摘要
   - 文案分析
   - 文案改写（品牌：立时）
   - 飞书多维表格链接
6. 下载结果 JSON 文件

---

## 🎯 为什么 Streamlit Cloud 更好？

| 对比项 | Render 免费版 | Streamlit Cloud |
|--------|--------------|-----------------|
| 部署难度 | ⚠️ 复杂（需配置） | ✅ 简单（1 分钟） |
| 系统库 | ❌ 有限制（dbus-python 问题） | ✅ 无限制 |
| 内存 | ❌ 512MB（不够用） | ✅ 1GB+ |
| 视频处理 | ⚠️ 需手动配置 | ✅ 原生支持 |
| HTTPS | ⚠️ 需配置 | ✅ 自动提供 |
| AI 应用 | ⚠️ 通用平台 | ✅ 专为 AI 设计 |
| 费用 | ✅ 免费 | ✅ 免费 |

**结论：对于 LangGraph + AI 应用，Streamlit Cloud 是最佳选择！**

---

## 📊 功能对比

两个版本功能完全相同：

| 功能 | Render 版本 | Streamlit 版本 |
|------|------------|----------------|
| 视频文案提取 | ✅ | ✅ |
| 文案摘要 | ✅ | ✅ |
| 文案分析 | ✅ | ✅ |
| 文案改写 | ✅ | ✅ |
| 飞书多维表格 | ✅ | ✅ |
| Web 界面 | ✅ | ✅ |
| HTTPS | ✅ | ✅ |
| 免费部署 | ✅ | ✅ |

---

## 🎨 Streamlit 版本额外优势

### UI/UX
- 🎨 现代化暗色主题
- 📱 响应式设计
- 🖼️ 实时预览
- 📊 结果可视化
- 💾 一键下载

### 用户体验
- ✅ 更流畅的交互
- ✅ 更好的错误提示
- ✅ 进度条显示
- ✅ 自动刷新
- ✅ 移动端支持

---

## 🐛 如果遇到问题

### 问题 1：部署失败
**解决方案：**
1. 确认 GitHub 仓库是公开的
2. 检查 `app_streamlit.py` 文件是否存在
3. 检查 `requirements_streamlit.txt` 是否正确

### 问题 2：应用启动慢
**解决方案：**
- 第一次启动需要安装依赖，等待 2-3 分钟
- 后续启动会快很多（有缓存）

### 问题 3：视频上传失败
**解决方案：**
1. 检查视频大小（建议 <100MB）
2. 检查视频格式（支持 mp4, mov, avi, flv, webm, mkv）
3. 查看日志（Settings → Logs）

### 问题 4：处理失败
**解决方案：**
1. 检查环境变量是否配置正确
2. 查看 Streamlit 日志
3. 确认 Coze 和飞书集成已配置

---

## 📚 相关文档

- 📖 [Streamlit Cloud 部署指南](STREAMLIT_DEPLOY.md)
- 📖 [Requirements 维护指南](REQUIREMENTS_GUIDE.md)
- 📖 Streamlit 官方文档：https://docs.streamlit.io

---

## 🎉 立即开始

**访问：https://streamlit.io/cloud**

**选择你的 GitHub 仓库，点击 Deploy，1 分钟后就能使用了！**

---

## 💡 小贴士

1. **首次部署**：建议先在小文件上测试（<10MB 视频）
2. **性能优化**：如果有大文件，建议本地处理后再上传
3. **历史记录**：Streamlit 会自动保存会话，可以查看历史
4. **分享应用**：部署后可以直接分享 URL 给他人使用

---

**祝部署成功！** 🚀

有任何问题，请查看 [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md) 详细文档。
