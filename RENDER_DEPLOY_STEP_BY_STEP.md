# 🆓 Render免费部署 - 超详细步骤

## 第1步：创建GitHub仓库（3分钟）

### 1.1 访问GitHub
打开浏览器，访问：https://github.com

### 1.2 登录/注册
- 如果没有账号，点击 "Sign up" 注册
- 如果已有账号，点击 "Sign in" 登录

### 1.3 创建新仓库
1. 点击右上角的 "+" 号
2. 选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `video-extraction`（或你喜欢的名字）
   - **Description**: `视频文案提取系统`
   - **Public/Private**: 选择 **Public**（免费）
   - **勾选**: "Add a README file"
4. 点击 "Create repository"

### 1.4 复制仓库地址
创建成功后，复制你的仓库地址，例如：
```
https://github.com/yourusername/video-extraction.git
```

---

## 第2步：推送代码到GitHub（2分钟）

### 2.1 给脚本添加执行权限
```bash
chmod +x push_to_github.sh
```

### 2.2 运行推送脚本
```bash
./push_to_github.sh
```

### 2.3 按提示操作
1. 脚本会提示输入GitHub仓库地址
2. 粘贴你刚才复制的地址
3. 按回车

### 2.4 输入提交信息
- 可以直接按回车使用默认提交信息
- 或者输入自定义的提交信息
- 按回车

### 2.5 等待推送完成
- 会提示输入GitHub用户名和密码
- **注意**：GitHub现在需要使用Personal Access Token
- 如果提示密码错误，见下方"常见问题"

### 2.6 验证
访问你的GitHub仓库，确认代码已推送成功！

---

## 第3步：在Render部署（5分钟）

### 3.1 注册Render账号
1. 访问：https://render.com
2. 点击 "Sign Up"
3. 选择 "Sign up with GitHub"
4. 授权Render访问你的GitHub账号

### 3.2 创建Web Service
1. 登录后，点击右上角的 "+"
2. 选择 "New Web Service"
3. 在 "Connect a repository" 部分：
   - 选择你的GitHub账号
   - 找到 "video-extraction" 仓库
   - 点击 "Connect"

### 3.3 配置服务
在配置页面填写以下信息：

**Name**: `video-extraction`

**Region**: 选择离你最近的区域（如Singapore）

**Branch**: `main`

**Runtime**: `Python 3`

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### 3.4 配置环境变量
向下滚动到 "Environment Variables" 部分，点击 "Add Environment Variable"

添加以下变量：

| Key | Value |
|-----|-------|
| `PYTHONPATH` | `/opt/render/project/src` |
| `PORT` | `5000` |

### 3.5 配置自动部署（可选）
- 勾选 "Auto-Deploy"（每次推送代码自动重新部署）

### 3.6 创建服务
点击页面底部的 "Create Web Service" 按钮

### 3.7 等待部署
- 部署过程约需要3-5分钟
- 可以看到实时日志
- 绿色对勾✅表示部署成功

### 3.8 获取公网URL
部署成功后，页面会显示你的应用URL，例如：
```
https://video-extraction.onrender.com
```

---

## 第4步：测试访问（1分钟）

### 4.1 打开浏览器
访问你的Render提供的URL

### 4.2 测试功能
1. 上传一个测试视频
2. 点击"开始分析"
3. 等待处理完成
4. 查看飞书链接

---

## ✅ 完成！

现在你拥有一个：
- ✅ 永久免费的网页应用
- ✅ 全球可访问的公网URL
- ✅ 自动HTTPS加密
- ✅ 自动持续部署

---

## 🔗 分享链接

把你的Render URL分享给任何人：
```
https://video-extraction.onrender.com
```

他们不需要任何账号或登录，直接就能使用！

---

## 📝 常见问题

### Q1: GitHub推送时提示密码错误？
**A**: GitHub现在需要使用Personal Access Token
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 "repo" 权限
4. 点击 "Generate token"
5. 复制token（只显示一次！）
6. 推送时，用户名输入GitHub用户名，密码输入token

### Q2: Render部署失败？
**A**: 检查以下内容：
- 确保 `render.yaml` 文件在项目根目录
- 确保所有依赖都在 `requirements.txt` 中
- 查看Render的部署日志，定位错误

### Q3: 启动命令错误？
**A**: 确保：
- 已安装gunicorn（在requirements.txt中）
- start command正确：`gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
- 环境变量PYTHONPATH设置正确

### Q4: 部署成功但访问不了？
**A**: 等待1-2分钟，Render可能还在初始化
- 查看服务状态是否为 "Live"
- 查看是否有错误日志

### Q5: 如何更新代码？
**A**: 两种方式：
1. **自动部署**：勾选了"Auto-Deploy"，推送代码后自动部署
2. **手动部署**：在Render dashboard点击 "Manual Deploy"

---

## 🎯 下一步

部署完成后，你可以：
- 📱 把URL分享给朋友
- 🌐 放到个人网站
- 💼 用于商业项目
- 🔄 持续更新功能

---

## 📞 需要帮助？

如果遇到问题，请告诉我具体在哪一步卡住了，我会帮你解决！
