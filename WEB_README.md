# 视频文案提取与分析系统 - Web版

这是一个基于Flask的视频文案提取与分析Web应用，用户可以通过浏览器上传视频文件，自动提取文案、分析痛点、生成5种风格的改写文案，并保存到飞书多维表格。

## 功能特性

- 📹 **视频上传**：支持多种视频格式（MP4、MOV、AVI、FLV、WEBM、MKV）
- 🎯 **文案提取**：使用多模态AI自动识别视频中的文字内容
- 📝 **文案摘要**：智能生成文案的核心摘要
- 🔬 **深度分析**：分析用户痛点、人群画像和成功原因
- ✍️ **5种改写**：生成不同风格的改写文案（痛点直击、情感共鸣、数据说服、场景描述、简洁有力）
- 📊 **飞书集成**：自动保存到飞书多维表格，方便后续管理
- 💻 **Web界面**：美观的用户界面，支持拖拽上传

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

**方式一：使用启动脚本**
```bash
chmod +x start_web.sh
./start_web.sh
```

**方式二：直接运行**
```bash
python3 app.py
```

### 3. 访问应用

打开浏览器，访问：`http://localhost:5000`

## 使用说明

### 上传视频

1. 点击上传区域或拖拽视频文件到上传区域
2. 支持的视频格式：MP4、MOV、AVI、FLV、WEBM、MKV
3. 最大文件大小：500MB
4. 点击"开始分析"按钮

### 查看结果

处理完成后，系统会自动显示：

1. **提取的文案**：视频中的原始文字内容
2. **文案摘要**：文案的核心内容摘要
3. **文案分析**：
   - 用户痛点分析
   - 人群画像分析
   - 成功原因分析
4. **5种改写文案**：
   - 改写1：痛点直击型
   - 改写2：情感共鸣型
   - 改写3：数据说服型
   - 改写4：场景化描述型
   - 改写5：简洁有力型
5. **飞书表格链接**：点击链接查看完整数据

### 复制内容

每个结果卡片都有"复制"按钮，点击即可复制内容到剪贴板。

## 技术栈

- **后端**：Python 3 + Flask
- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap 5
- **AI引擎**：LangGraph + LangChain
- **多模态模型**：doubao-seed-1-6-vision-250815, doubao-seed-1-8-251228
- **数据存储**：飞书多维表格

## 项目结构

```
.
├── app.py                      # Flask主应用
├── start_web.sh                # 启动脚本
├── requirements.txt            # Python依赖
├── templates/
│   └── index.html             # 前端页面
├── static/
│   ├── css/
│   │   └── style.css          # 样式文件
│   └── js/
│       └── main.js            # JavaScript逻辑
├── src/
│   ├── graphs/                # 工作流定义
│   │   ├── graph.py          # 主图编排
│   │   ├── state.py          # 状态定义
│   │   └── nodes/            # 节点实现
│   │       ├── video_text_extraction_node.py
│   │       ├── text_summary_node.py
│   │       ├── text_analysis_node.py
│   │       ├── text_rewrite_node.py
│   │       └── feishu_doc_write_node.py
│   └── utils/                 # 工具类
└── config/                    # 配置文件
    ├── video_text_extraction_cfg.json
    ├── text_summary_cfg.json
    ├── text_analysis_cfg.json
    └── text_rewrite_cfg.json
```

## 配置说明

### 修改端口

在 `app.py` 文件中修改：

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 修改port为你想要的端口
```

### 修改上传限制

在 `app.py` 文件中修改：

```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
```

### 修改上传目录

在 `app.py` 文件中修改：

```python
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # 修改为你想要的目录
```

## 飞书配置

系统会自动使用集成的飞书技能创建多维表格。如需自定义：

1. 确保已配置飞书技能凭证
2. 查看飞书多维表格技能文档

## 常见问题

### Q: 上传视频后提示"处理失败"怎么办？

A: 请检查：
1. 视频格式是否支持
2. 视频大小是否超过500MB
3. 网络连接是否正常
4. 查看控制台错误日志

### Q: 如何修改品牌名称？

A: 在 `config/text_rewrite_cfg.json` 文件中修改提示词中的品牌名称。

### Q: 处理时间很长怎么办？

A: 视频处理时间取决于视频长度和内容复杂度，建议：
1. 使用较短的测试视频
2. 确保网络连接稳定
3. 等待处理完成

### Q: 如何查看处理日志？

A: 查看控制台输出或检查 `/app/work/logs/bypass/app.log` 文件。

## 开发说明

### 添加新功能

1. 在 `src/graphs/nodes/` 下创建新的节点文件
2. 在 `src/graphs/state.py` 中定义状态
3. 在 `src/graphs/graph.py` 中添加节点到工作流
4. 在 `app.py` 中添加对应的API接口

### 自定义前端样式

修改 `static/css/style.css` 文件。

### 自定义前端逻辑

修改 `static/js/main.js` 文件。

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系开发团队。
