import os
import json
import logging
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import TextSummaryInput, TextSummaryOutput

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

def text_summary_node(
    state: TextSummaryInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TextSummaryOutput:
    """
    title: 文案摘要生成
    desc: 对提取的文案内容进行分析，生成摘要
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取大模型配置
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
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
            max_completion_tokens=llm_config.get("max_completion_tokens", 4096),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 提取文本内容
        text_summary = get_text_content(response.content).strip()
        
        logger.info(f"成功生成文案摘要，长度: {len(text_summary)} 字符")
        
        return TextSummaryOutput(text_summary=text_summary)
        
    except Exception as e:
        logger.error(f"文案摘要生成失败: {str(e)}")
        raise Exception(f"文案摘要生成失败: {str(e)}")
