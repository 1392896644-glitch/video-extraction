from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys
import json
import logging
from coze_coding_dev_sdk.s3 import S3SyncStorage

# 添加src目录到Python路径（兼容Render部署环境）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from graphs.graph import main_graph
from graphs.state import GraphInput
from utils.file.file import File

# 配置日志（降低日志级别以减少内存占用）
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 只在关键地方输出 INFO

# 初始化对象存储（使用 Coze S3 代理）
storage = S3SyncStorage(
    endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
    access_key="",
    secret_key="",
    bucket_name=os.getenv("COZE_BUCKET_NAME"),
    region="cn-beijing",
)

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB（降低以减少内存压力）

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
        
        # 保存文件到临时目录
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"视频文件已保存到临时目录: {filepath}")
        
        # 上传到对象存储（使用分块上传减少内存使用）
        logger.info("正在上传视频到对象存储...")
        try:
            file_key = storage.stream_upload_file(
                fileobj=open(filepath, 'rb'),
                file_name=filename,
                content_type=f"video/{filename.rsplit('.', 1)[1].lower()}"
            )
            logger.info(f"视频已上传到对象存储，key: {file_key}")
            
            # 生成签名 URL（有效期 1 小时）
            video_url = storage.generate_presigned_url(key=file_key, expire_time=3600)
            logger.info(f"视频签名 URL: {video_url}")
        except Exception as e:
            logger.error(f"对象存储上传失败: {str(e)}")
            return jsonify({'success': False, 'error': f'视频上传失败（内存不足或网络错误）: {str(e)}'}), 500
        
        # 调用工作流
        logger.info("开始调用工作流...")
        result = run_workflow(video_url)
        
        logger.info("工作流执行完成")
        
        # 检查是否有错误
        if result.get('error'):
            logger.warning(f"工作流执行有错误: {result.get('error')}")
        
        # 返回结果
        response_data = {
            'success': not bool(result.get('error')),
            'feishu_url': result.get('feishu_url', ''),
            'extracted_text': result.get('extracted_text', ''),
            'text_summary': result.get('text_summary', ''),
            'text_analysis': result.get('text_analysis', ''),
            'rewritten_texts': result.get('rewritten_texts', [])
        }
        
        if result.get('error'):
            response_data['error'] = result.get('error')
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

def run_workflow(video_url):
    """运行工作流"""
    try:
        logger.info("=" * 80)
        logger.info("开始运行工作流")
        logger.info(f"使用视频 URL 调用工作流: {video_url}")

        # 创建File对象（使用对象存储的 URL）
        video_file = File(url=video_url, file_type="video")

        # 构建输入数据
        input_data = GraphInput(video_file=video_file)
        logger.info(f"构建输入数据: {input_data}")

        # 调用工作流（不需要手动创建Runtime和Context）
        logger.info("调用 main_graph.invoke()")
        result = main_graph.invoke(input_data, config={})
        logger.info("工作流调用完成")

        # 检查返回值类型
        logger.info(f"工作流返回值类型: {type(result)}")
        
        if hasattr(result, 'model_dump'):
            # 如果是 Pydantic 模型，转换为字典
            logger.info("将 Pydantic 模型转换为字典")
            result_dict = result.model_dump()
            logger.info(f"返回结果: {result_dict}")
            logger.info("=" * 80)
            return result_dict
        elif isinstance(result, dict):
            # 如果是字典，直接返回
            logger.info(f"返回结果（字典）: {result}")
            logger.info("=" * 80)
            return result
        else:
            # 其他情况，尝试转换为字典
            logger.warning(f"工作流返回未知类型: {type(result)}")
            result_dict = dict(result)
            logger.info(f"转换后的结果: {result_dict}")
            logger.info("=" * 80)
            return result_dict

    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"❌ 工作流执行失败: {str(e)}")
        logger.error(f"   异常类型: {type(e).__name__}")
        logger.error(f"   异常详情: {str(e)}", exc_info=True)
        logger.error("=" * 80)
        # 返回错误信息
        return {
            'error': str(e),
            'feishu_url': '',
            'extracted_text': '',
            'text_summary': '',
            'text_analysis': '',
            'rewritten_texts': []
        }

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

@app.route('/debug')
def debug():
    """调试信息 - 显示环境变量和配置状态"""
    from coze_workload_identity import Client
    
    debug_info = {
        'environment_variables': {
            'COZE_BUCKET_ENDPOINT_URL': '✅ 已配置' if os.getenv('COZE_BUCKET_ENDPOINT_URL') else '❌ 未配置',
            'COZE_BUCKET_NAME': '✅ 已配置' if os.getenv('COZE_BUCKET_NAME') else '❌ 未配置',
            'COZE_WORKLOAD_IDENTITY_API_KEY': '✅ 已配置' if os.getenv('COZE_WORKLOAD_IDENTITY_API_KEY') else '❌ 未配置',
            'COZE_WORKLOAD_IDENTITY_CLIENT_ID': '✅ 已配置' if os.getenv('COZE_WORKLOAD_IDENTITY_CLIENT_ID') else '❌ 未配置',
            'COZE_WORKLOAD_IDENTITY_ENDPOINT': '✅ 已配置' if os.getenv('COZE_WORKLOAD_IDENTITY_ENDPOINT') else '⚠️ 未配置（可选）',
        },
        'feishu_integration': {
            'status': '检查中...'
        }
    }
    
    # 尝试获取飞书凭证
    try:
        client = Client()
        feishu_token = client.get_integration_credential("integration-feishu-base")
        debug_info['feishu_integration'] = {
            'status': '✅ 成功获取',
            'token_preview': f"{feishu_token[:20]}..." if feishu_token else '❌ 未配置',
            'has_token': bool(feishu_token)
        }
    except Exception as e:
        debug_info['feishu_integration'] = {
            'status': '❌ 获取失败',
            'error': str(e),
            'has_token': False
        }
    
    return jsonify(debug_info)

if __name__ == '__main__':
    print("=" * 50)
    print("🎬 视频文案提取系统启动中...")
    print("🌐 访问地址: http://localhost:5000")
    print("✨ 功能: 提取视频文案、生成摘要、分析痛点、生成5条改写文案")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
