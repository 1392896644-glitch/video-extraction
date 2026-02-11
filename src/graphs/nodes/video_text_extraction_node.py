import os
import json
import logging
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import VideoTextExtractionInput, VideoTextExtractionOutput

logger = logging.getLogger(__name__)

def get_text_content(content) -> str:
    """安全提取AIMessage的文本内容"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        if content and isinstance(content[0], str):
            return " ".join(content)
        else:
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            return " ".join(text_parts)
    return str(content)

def video_text_extraction_node(
    state: VideoTextExtractionInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> VideoTextExtractionOutput:
    """
    title: 视频文案提取
    desc: 从上传的视频文件中识别并提取文案文字内容
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 获取视频文件URL
    video_url = state.video_file.url
    logger.info(f"处理视频文件: {video_url}")
    
    # 读取大模型配置
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
    cfg_file = os.path.join(workspace_path, config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)
    
    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up_template = _cfg.get("up", "")
    
    # 渲染用户提示词
    up_tpl = Template(up_template)
    user_prompt_content = up_tpl.render({"video_url": video_url})
    
    try:
        # 初始化LLM客户端
        client = LLMClient(ctx=ctx)
        
        # 构建多模态消息
        video_input = [
            {"type": "text", "text": user_prompt_content},
            {"type": "video_url", "video_url": {"url": video_url}}
        ]
        
        # 构建消息
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=video_input)
        ]
        
        # 调用大模型
        response = client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-1-6-vision-250815"),
            temperature=llm_config.get("temperature", 0.3),
            top_p=llm_config.get("top_p", 0.9),
            max_completion_tokens=llm_config.get("max_completion_tokens", 8192),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 提取文本内容
        extracted_text = get_text_content(response.content).strip()
        
        logger.info(f"成功从视频提取文案，长度: {len(extracted_text)} 字符")
        
        return VideoTextExtractionOutput(extracted_text=extracted_text)
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"视频文案提取失败: {error_msg}")
        raise Exception(f"视频文案提取失败: {error_msg}")
