from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.video_text_extraction_node import video_text_extraction_node
from graphs.nodes.text_summary_node import text_summary_node
from graphs.nodes.text_analysis_node import text_analysis_node
from graphs.nodes.text_rewrite_node import text_rewrite_node

# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
# 1. 视频文案提取节点（大模型Agent）
builder.add_node(
    "video_text_extraction",
    video_text_extraction_node,
    metadata={"type": "agent", "llm_cfg": "config/video_text_extraction_cfg.json"}
)

# 2. 文案摘要生成节点（大模型Agent）
builder.add_node(
    "text_summary",
    text_summary_node,
    metadata={"type": "agent", "llm_cfg": "config/text_summary_cfg.json"}
)

# 3. 文案分析节点（大模型Agent）
builder.add_node(
    "text_analysis",
    text_analysis_node,
    metadata={"type": "agent", "llm_cfg": "config/text_analysis_cfg.json"}
)

# 4. 文案改写节点（大模型Agent）- 生成5条不同文案
builder.add_node(
    "text_rewrite",
    text_rewrite_node,
    metadata={"type": "agent", "llm_cfg": "config/text_rewrite_cfg.json"}
)

# 设置入口点
builder.set_entry_point("video_text_extraction")

# 添加边：视频文案提取完成后，并行执行摘要生成、文案分析和文案改写
builder.add_edge("video_text_extraction", "text_summary")
builder.add_edge("video_text_extraction", "text_analysis")
builder.add_edge("video_text_extraction", "text_rewrite")

# 添加边：摘要生成、文案分析和文案改写都完成后，直接结束（移除飞书节点）
builder.add_edge(["text_summary", "text_analysis", "text_rewrite"], END)

# 编译图
main_graph = builder.compile()
