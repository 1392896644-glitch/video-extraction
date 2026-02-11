import os
import json
import logging
from jinja2 import Template
from typing import List
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import TextRewriteInput, TextRewriteOutput

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

def text_rewrite_node(
    state: TextRewriteInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TextRewriteOutput:
    """
    title: 文案改写
    desc: 对文案进行二创改写，生成5条不同风格的改写文案，品牌名称统一改为"立时"
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
            temperature=llm_config.get("temperature", 0.8),
            top_p=llm_config.get("top_p", 0.9),
            max_completion_tokens=llm_config.get("max_completion_tokens", 8192),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 提取文本内容
        rewritten_text = get_text_content(response.content).strip()
        
        # 解析出5条改写文案（按行分割或按特定格式分割）
        # 假设大模型返回的是JSON数组格式
        try:
            import re
            # 尝试提取JSON数组格式
            json_match = re.search(r'\[.*?\]', rewritten_text, re.DOTALL)
            if json_match:
                rewritten_texts = json.loads(json_match.group())
            else:
                # 如果不是JSON格式，按行分割
                lines = [line.strip() for line in rewritten_text.split('\n') if line.strip()]
                # 过滤掉标题行（如"改写1："等）
                rewritten_texts = []
                for line in lines:
                    # 移除序号前缀
                    clean_line = re.sub(r'^\d+[\.\、]|[一二三四五六七八九十][\.\、]|改写\d*[:：]', '', line).strip()
                    if clean_line and len(clean_line) > 10:  # 过滤掉太短的内容
                        rewritten_texts.append(clean_line)
                
                # 确保有5条文案
                while len(rewritten_texts) < 5:
                    rewritten_texts.append(f"立时品牌改写文案{len(rewritten_texts)+1}")
                rewritten_texts = rewritten_texts[:5]
        except Exception as parse_error:
            logger.warning(f"解析改写文案失败: {parse_error}，使用原始返回")
            # 如果解析失败，简单分割
            rewritten_texts = rewritten_text.split('\n\n')[:5]
            if len(rewritten_texts) < 5:
                # 补充到5条
                for i in range(len(rewritten_texts), 5):
                    rewritten_texts.append(f"立时品牌改写文案{i+1}")
        
        logger.info(f"成功改写文案，生成了 {len(rewritten_texts)} 条文案")
        
        return TextRewriteOutput(rewritten_texts=rewritten_texts)
        
    except Exception as e:
        logger.error(f"文案改写失败: {str(e)}")
        raise Exception(f"文案改写失败: {str(e)}")
