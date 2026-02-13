# 🚀 Streamlit Cloud 部署指南

## ✨ 为什么选择 Streamlit Cloud？

- ✅ **完全免费** - 无需信用卡
- ✅ **1 分钟部署** - 超级简单
- ✅ **专为 AI 应用设计** - 完美支持 LangGraph
- ✅ **无需系统库** - 避免 dbus-python 问题
- ✅ **内存充足** - 1GB+ 免费内存
- ✅ **自动 HTTPS** - 无需配置

---

## 📋 部署步骤（3 步完成）

### 步骤 1：准备代码

确保你已经：
1. ✅ 有 GitHub 账号
2. ✅ 代码已推送到 GitHub
3. ✅ 本地测试成功（可选）

### 步骤 2：创建 Streamlit 账号

1. 访问：https://streamlit.io/cloud
2. 点击 "Sign up" 或 "Sign in with GitHub"
3. 授权 GitHub 访问

### 步骤 3：部署应用

1. 在 Streamlit Cloud 点击 "New app"
2. 选择 GitHub 仓库
3. 选择分支（main）
4. 配置：
   - **Main file path**: `app_streamlit.py`
   - **Python version**: `3.12` 或 `3.13`
   - **Dependencies**: `requirements_streamlit.txt`
5. 点击 "Deploy"

**等待 1-2 分钟，部署完成！** 🎉

---

## 🔧 环境变量配置

在 Streamlit Cloud 的 "Settings" → "Secrets" 中添加：

```
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_WORKLOAD_IDENTITY_CLIENT_ID=your_client_id
COZE_WORKLOAD_IDENTITY_CLIENT_SECRET=your_client_secret
COZE_BUCKET_ENDPOINT_URL=your_bucket_url
COZE_BUCKET_NAME=your_bucket_name
```

**如何获取这些值？**
1. 访问 Coze 平台
2. 进入你的项目设置
3. 找到 "集成" → "工作负载身份"
4. 复制 API Key、Client ID、Client Secret

---

## 🎯 应用特点

### 功能
1. 🎬 视频文案提取
2. 📋 文案摘要生成
3. 🔍 文案分析（痛点、人群画像）
4. ✍️ 文案改写（品牌：立时）
5. 📊 飞书多维表格保存

### 界面
- 🎨 现代化暗色主题
- 📱 响应式设计
- 🖼️ 实时视频预览
- 📊 结果可视化展示
- 💾 一键下载结果

---

## 📊 对比：Render vs Streamlit Cloud

| 项目 | Render 免费版 | Streamlit Cloud |
|------|--------------|-----------------|
| 部署难度 | 复杂（需配置） | 简单（1 分钟） |
| 系统库 | 有限制 | 无限制 |
| 内存 | 512MB | 1GB+ |
| 视频 | 需手动配置 | 原生支持 |
| HTTPS | 需配置 | 自动提供 |
| 费用 | 免费 | 免费 |
| 适用场景 | 复杂应用 | AI 应用 |

**结论：对于 LangGraph + AI 应用，Streamlit Cloud 是最佳选择！**

---

## 🐛 常见问题

### Q: 部署失败怎么办？
A: 检查：
1. GitHub 仓库是否公开
2. `app_streamlit.py` 文件是否存在
3. `requirements_streamlit.txt` 是否正确

### Q: 应用启动慢？
A: 第一次启动需要安装依赖，等待 2-3 分钟即可。

### Q: 视频上传失败？
A: 检查：
1. 视频大小（建议 <100MB）
2. 视频格式（支持 mp4, mov, avi, flv, webm, mkv）

### Q: 如何查看日志？
A: 在 Streamlit Cloud 的 "Logs" 标签页查看。

---

## 🚀 后续优化

### 性能优化
- ✅ 添加缓存（st.cache_data）
- ✅ 使用异步加载
- ✅ 优化视频处理

### 功能增强
- ✅ 批量处理
- ✅ 历史记录
- ✅ 结果对比
- ✅ 自定义配置

### UI 优化
- ✅ 加载动画
- ✅ 进度条
- ✅ 错误提示
- ✅ 成功提示

---

## 📞 获取帮助

- 📖 Streamlit 文档：https://docs.streamlit.io
- 💬 Streamlit 社区：https://discuss.streamlit.io
- 🐛 提交问题：https://github.com/streamlit/streamlit/issues

---

## 🎉 开始部署

**立即访问：https://streamlit.io/cloud**

**祝部署成功！** 🚀
