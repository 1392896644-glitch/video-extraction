# 🌐 公网部署指南 - 让全世界都能访问

## 🎯 目标
创建一个任何人通过链接都能访问的网页版视频文案提取系统

---

## 📦 方案对比

| 方案 | 难度 | 费用 | 稳定性 | 推荐度 |
|------|------|------|--------|--------|
| 云服务器 | ⭐⭐⭐ | 低/中 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Render/Railway | ⭐⭐ | 免费套餐 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 内网穿透(ngrok) | ⭐ | 免费 | ⭐⭐ | ⭐⭐⭐ |

---

## 🚀 方案一：云服务器部署（推荐）

### 步骤1：购买云服务器
- 阿里云：https://www.aliyun.com
- 腾讯云：https://cloud.tencent.com
- 推荐配置：2核4G，1M带宽

### 步骤2：连接服务器
```bash
ssh root@你的服务器IP
```

### 步骤3：上传代码
```bash
# 在本地电脑上
scp -r /workspace/projects root@服务器IP:/root/
```

### 步骤4：在服务器上安装环境
```bash
# 安装Python
yum install python3 python3-pip -y  # CentOS
# 或
apt install python3 python3-pip -y  # Ubuntu

# 安装依赖
cd /root/projects
pip3 install -r requirements.txt

# 安装生产服务器
pip3 install gunicorn
```

### 步骤5：启动服务
```bash
cd /root/projects
export PYTHONPATH=/root/projects/src:$PYTHONPATH
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 步骤6：配置域名（可选）
1. 购买域名（阿里云、腾讯云）
2. 配置DNS解析：A记录指向服务器IP
3. 使用Nginx配置域名访问

### 步骤7：配置防火墙
```bash
# 开放5000端口
firewall-cmd --permanent --add-port=5000/tcp
firewall-cmd --reload
```

### 完成！
访问：`http://你的服务器IP:5000`

---

## 🌟 方案二：Render部署（零成本）

### 步骤1：注册账号
访问：https://render.com

### 步骤2：创建Web Service
1. 点击 "New +" → "Web Service"
2. 连接GitHub账号
3. 将代码推送到GitHub
4. 配置构建和部署

### 步骤3：配置环境变量
```
PYTHONPATH=/app/src
```

### 步骤4：配置启动命令
```
gunicorn app:app
```

### 完成！
Render会自动分配一个公网URL，例如：`https://your-app.onrender.com`

---

## ⚡ 方案三：内网穿透（临时测试）

### 使用ngrok

1. **安装ngrok**
```bash
# 下载ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip
```

2. **注册ngrok账号**
访问：https://ngrok.com 注册并获取authtoken

3. **配置ngrok**
```bash
./ngrok config add-authtoken 你的token
```

4. **启动服务**
```bash
# 启动Flask应用
cd /workspace/projects
export PYTHONPATH=/workspace/projects/src:$PYTHONPATH
python3 app.py &

# 启动ngrok
./ngrok http 5000
```

5. **获取公网URL**
ngrok会显示一个临时的公网URL，例如：
```
Forwarding: https://xxxx-xx-xx-xx-xx.ngrok.io -> http://localhost:5000
```

### 完成！
访问ngrok提供的URL即可！

---

## 🔧 方案四：使用Docker部署

### 创建Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /tmp/uploads

ENV PYTHONPATH=/app/src

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t video-extraction .

# 运行容器
docker run -d -p 5000:5000 video-extraction
```

---

## 📱 访问方式

### 本地测试
```
http://localhost:5000
```

### 云服务器
```
http://你的服务器IP:5000
或
http://你的域名.com
```

### Render/Railway
```
https://your-app.onrender.com
或
https://your-app.railway.app
```

### ngrok（临时）
```
https://xxxx-xx-xx-xx-xx.ngrok.io
```

---

## 🔒 安全建议

1. **使用HTTPS**
   - 配置SSL证书（Let's Encrypt）
   - 使用Nginx反向代理

2. **限制访问**
   - 添加身份验证
   - IP白名单
   - 访问频率限制

3. **数据安全**
   - 定期备份数据
   - 使用环境变量存储敏感信息

---

## 🎯 最推荐方案

**个人使用**：Render/Railway（免费套餐）
- 零成本
- 自动HTTPS
- 全球CDN

**商业使用**：云服务器
- 完全控制
- 性能更好
- 可扩展

**临时测试**：ngrok
- 立即可用
- 无需部署
- 临时URL

---

## 📞 需要帮助？

根据你的需求选择方案，我可以提供详细的配置帮助！
