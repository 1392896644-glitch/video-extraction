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
from graphs.nodes.feishu_doc_write_node import feishu_doc_write_node

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

# 5. 飞书文档写入节点（普通节点）
builder.add_node("feishu_doc_write", feishu_doc_write_node)

# 设置入口点
builder.set_entry_point("video_text_extraction")

# 添加边：串行执行，减少内存峰值
builder.add_edge("video_text_extraction", "text_summary")
builder.add_edge("text_summary", "text_analysis")
builder.add_edge("text_analysis", "text_rewrite")
builder.add_edge("text_rewrite", "feishu_doc_write")

# 添加边：飞书文档写入完成后结束
builder.add_edge("feishu_doc_write", END)

# 编译图
main_graph = builder.compile()
