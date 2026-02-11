from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys
import json
import logging

# 添加src目录到Python路径（兼容Render部署环境）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.graph import main_graph
from graphs.state import GraphInput
from utils.file.file import File

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的视频格式
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'flv', 'webm', 'mkv'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """处理视频上传并调用工作流"""
    try:
        # 检查是否有文件
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': '没有上传文件'}), 400
        
        file = request.files['video']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({'success': False, 'error': '未选择文件'}), 400
        
        # 检查文件格式
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': '不支持的文件格式，请上传 mp4, mov, avi, flv, webm 或 mkv 格式的视频'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"视频文件已保存: {filepath}")
        
        # 调用工作流
        logger.info("开始调用工作流...")
        result = run_workflow(filepath)
        
        logger.info("工作流执行完成")
        
        # 只返回飞书URL
        return jsonify({
            'success': True,
            'feishu_url': result.get('feishu_url', '')
        })
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

def run_workflow(video_path):
    """运行工作流"""
    try:
        # 构建输入
        abs_path = os.path.abspath(video_path)
        
        # 创建File对象
        video_file = File(url=f"file://{abs_path}", file_type="video")
        
        # 构建输入数据
        input_data = GraphInput(video_file=video_file)
        
        # 创建上下文
        context = Context()
        
        # 调用工作流
        runtime = Runtime(context)
        result = main_graph.invoke(input_data, config={}, runtime=runtime)
        
        # 只返回飞书URL
        return result
        
    except Exception as e:
        logger.error(f"工作流执行失败: {str(e)}", exc_info=True)
        raise

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("=" * 50)
    print("🎬 视频文案提取系统启动中...")
    print("🌐 访问地址: http://localhost:5000")
    print("📊 飞书链接将在上传后显示")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
