import os
import json
import logging
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import TextAnalysisInput, TextAnalysisOutput

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

def text_analysis_node(
    state: TextAnalysisInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TextAnalysisOutput:
    """
    title: 文案分析
    desc: 深入分析文案中抓住的用户痛点、人群画像，以及文案数据表现好的原因
    integrations: 大语言模型
    """
    ctx = runtime.context
    
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
    user_prompt_content = up_tpl.render({"extracted_text": state.extracted_text})
    
    try:
        # 初始化LLM客户端
        client = LLMClient(ctx=ctx)
        
        # 构建消息
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=user_prompt_content)
        ]
        
        # 调用大模型
        response = client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-1-8-251228"),
            temperature=llm_config.get("temperature", 0.5),
            top_p=llm_config.get("top_p", 0.9),
            max_completion_tokens=llm_config.get("max_completion_tokens", 8192),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 提取文本内容
        text_analysis = get_text_content(response.content).strip()
        
        logger.info(f"成功生成文案分析，长度: {len(text_analysis)} 字符")
        
        return TextAnalysisOutput(text_analysis=text_analysis)
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"文案分析失败: {error_msg}")
        raise Exception(f"文案分析失败: {error_msg}")
