# 📤 推送代码到GitHub - 最后一步

## ✅ 代码已准备好！

你的GitHub仓库地址是：
```
https://github.com/1392896644-glitch/video-extraction
```

代码已经提交到本地仓库，现在需要推送到GitHub。

---

## 🚀 方法1：在命令行手动推送（推荐）

### 步骤1：配置Git用户信息（如果还没配置）
```bash
git config --global user.name "1392896644-glitch"
git config --global user.email "你的邮箱@example.com"
```

### 步骤2：添加远程仓库
```bash
git remote add origin https://github.com/1392896644-glitch/video-extraction.git
```

### 步骤3：推送代码
```bash
git push -u origin main
```

### 步骤4：输入GitHub凭据
- Username: `1392896644-glitch`
- Password: 输入你的Personal Access Token（不是GitHub密码！）

---

## 🔑 如何获取Personal Access Token？

GitHub现在要求使用Token而不是密码：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置名称：`video-extraction-deploy`
4. 选择过期时间：`No expiration`（永不过期）
5. 勾选权限：
   - ✅ `repo`（完整仓库访问权限）
   - ✅ `workflow`（如果需要）
6. 点击 "Generate token"
7. **重要**：复制token（只显示一次！）
8. 推送代码时，密码输入这个token

---

## 🚀 方法2：使用GitHub CLI（最简单）

### 步骤1：安装GitHub CLI
```bash
# 在命令行检查是否已安装
gh --version
```

如果没有安装：
- Windows: 从 https://cli.github.com 下载安装
- Mac: `brew install gh`
- Linux: `sudo apt install gh`

### 步骤2：登录GitHub
```bash
gh auth login
```
按提示操作：
- 选择 "GitHub.com"
- 选择 "HTTPS"
- 选择 "Login with a web browser"
- 浏览器会打开，点击 "Authorize"

### 步骤3：推送代码
```bash
git push -u origin main
```

使用GitHub CLI后，不需要输入密码！

---

## 🚀 方法3：使用SSH（最安全）

### 步骤1：生成SSH密钥
```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```
按回车使用默认设置

### 步骤2：添加SSH密钥到GitHub
```bash
# 复制公钥
cat ~/.ssh/id_ed25519.pub
```

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. 标题：`video-extraction`
4. 粘贴刚才复制的公钥
5. 点击 "Add SSH key"

### 步骤4：修改远程仓库地址为SSH
```bash
git remote set-url origin git@github.com:1392896644-glitch/video-extraction.git
```

### 步骤5：推送代码
```bash
git push -u origin main
```

---

## ✅ 推送成功后

1. 访问你的GitHub仓库：
   ```
   https://github.com/1392896644-glitch/video-extraction
   ```

2. 确认代码已上传，应该能看到：
   - `app.py`
   - `requirements.txt`
   - `templates/`
   - `src/`
   - 等等

3. 准备进行下一步：Render部署！

---

## ❓ 推送失败？

### 问题1：Permission denied (publickey)
**解决**：使用方法3配置SSH，或使用方法2的GitHub CLI

### 问题2：Authentication failed
**解决**：确认使用的是Personal Access Token，不是GitHub密码

### 问题3：remote origin already exists
**解决**：
```bash
git remote remove origin
git remote add origin https://github.com/1392896644-glitch/video-extraction.git
git push -u origin main
```

### 问题4：fatal: main does not exist
**解决**：
```bash
git branch -M main
git push -u origin main
```

---

## 📱 下一步

推送成功后，继续阅读：`RENDER_DEPLOY_STEP_BY_STEP.md`

在Render上部署，获得公网可访问的URL！

---

## 💡 提示

推荐使用**方法2（GitHub CLI）**，最简单且安全！
