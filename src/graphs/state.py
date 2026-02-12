from typing import Optional, List
from pydantic import BaseModel, Field
from utils.file.file import File

# 全局状态定义
class GlobalState(BaseModel):
    """全局状态定义"""
    video_file: File = Field(..., description="上传的视频文件")
    extracted_text: str = Field(default="", description="从视频中提取的文案内容")
    text_summary: str = Field(default="", description="文案摘要")
    text_analysis: str = Field(default="", description="文案分析（痛点、人群画像等）")
    rewritten_texts: List[str] = Field(default_factory=list, description="5条改写后的文案")
    feishu_app_token: str = Field(default="", description="飞书多维表格App Token")
    feishu_table_id: str = Field(default="", description="飞书数据表ID")
    record_id: str = Field(default="", description="创建的记录ID")
    feishu_url: str = Field(default="", description="飞书多维表格访问链接")

# 工作流输入
class GraphInput(BaseModel):
    """工作流的输入"""
    video_file: File = Field(..., description="上传的视频文件")

# 工作流输出
class GraphOutput(BaseModel):
    """工作流的输出"""
    feishu_app_token: str = Field(default="", description="飞书多维表格App Token")
    feishu_table_id: str = Field(default="", description="飞书数据表ID")
    record_id: str = Field(default="", description="创建的记录ID")
    feishu_url: str = Field(default="", description="飞书多维表格访问链接")
    extracted_text: str = Field(default="", description="提取的文案")
    text_summary: str = Field(default="", description="文案摘要")
    text_analysis: str = Field(default="", description="文案分析")
    rewritten_texts: List[str] = Field(default_factory=list, description="5条改写后的文案")
    error: Optional[str] = Field(default="", description="错误信息（如果失败）")

# 视频文案提取节点
class VideoTextExtractionInput(BaseModel):
    """视频文案提取节点的输入"""
    video_file: File = Field(..., description="上传的视频文件")

class VideoTextExtractionOutput(BaseModel):
    """视频文案提取节点的输出"""
    extracted_text: str = Field(..., description="从视频中提取的文案内容")

# 文案摘要生成节点
class TextSummaryInput(BaseModel):
    """文案摘要生成节点的输入"""
    extracted_text: str = Field(..., description="提取的文案内容")

class TextSummaryOutput(BaseModel):
    """文案摘要生成节点的输出"""
    text_summary: str = Field(..., description="文案摘要")

# 文案分析节点
class TextAnalysisInput(BaseModel):
    """文案分析节点的输入"""
    extracted_text: str = Field(..., description="提取的文案内容")

class TextAnalysisOutput(BaseModel):
    """文案分析节点的输出"""
    text_analysis: str = Field(..., description="文案分析内容，包括痛点、人群画像、数据好的原因")

# 文案改写节点
class TextRewriteInput(BaseModel):
    """文案改写节点的输入"""
    extracted_text: str = Field(..., description="提取的文案内容")

class TextRewriteOutput(BaseModel):
    """文案改写节点的输出"""
    rewritten_texts: List[str] = Field(..., description="5条不同的改写文案")

# 飞书文档写入节点
class FeishuDocWriteInput(BaseModel):
    """飞书文档写入节点的输入"""
    extracted_text: str = Field(..., description="提取的文案内容")
    text_summary: str = Field(..., description="文案摘要")
    text_analysis: str = Field(..., description="文案分析")
    rewritten_texts: List[str] = Field(..., description="5条改写后的文案")
    feishu_app_token: Optional[str] = Field(default="", description="飞书多维表格App Token（可选，为空则创建新Base）")
    feishu_table_id: Optional[str] = Field(default="", description="飞书数据表ID（可选，为空则创建新表）")

class FeishuDocWriteOutput(BaseModel):
    """飞书文档写入节点的输出"""
    feishu_app_token: str = Field(default="", description="飞书多维表格App Token")
    feishu_table_id: str = Field(default="", description="飞书数据表ID")
    record_id: str = Field(default="", description="创建的记录ID")
    feishu_url: str = Field(default="", description="飞书多维表格访问链接")
    error: Optional[str] = Field(default="", description="错误信息（如果失败）")
