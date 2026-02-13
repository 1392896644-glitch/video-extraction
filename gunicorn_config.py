# Gunicorn 配置文件
# 增加超时时间以适应大文件上传和视频处理

import os
import multiprocessing

# 工作进程数（根据Render免费版内存限制，只使用1个worker）
workers = 1

# 绑定地址（由环境变量 PORT 提供）
bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"

# 超时时间（秒）- 15分钟，足够处理大视频上传和AI处理
timeout = 900

# 保持连接时间
keepalive = 5

# 工作模式
worker_class = 'sync'

# 每个worker的线程数
threads = 2

# 最大请求数，达到后重启worker（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 100

# 日志级别
loglevel = 'info'

# 访问日志
accesslog = '-'

# 错误日志
errorlog = '-'

# 进程名称
proc_name = 'video-extraction'

# 是否启用后台模式
daemon = False

# 捕获输出
capture_output = True

# 重启时关闭worker
graceful_timeout = 30
