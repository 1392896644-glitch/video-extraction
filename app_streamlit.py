import streamlit as st
import os
import sys
import json
from typing import Optional

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from graphs.graph import main_graph
from graphs.state import GraphInput
from utils.file.file import File

# 页面配置
st.set_page_config(
    page_title="视频文案提取",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("🎬 视频文案提取与改写")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 配置")
    st.markdown("此应用会：")
    st.markdown("1. 提取视频中的文案")
    st.markdown("2. 生成文案摘要")
    st.markdown("3. 分析文案")
    st.markdown("4. 改写文案（品牌：立时）")
    st.markdown("5. 保存到飞书多维表格")
    st.markdown("---")
    st.info("💡 支持的视频格式：mp4, mov, avi, flv, webm, mkv")
    st.info("💡 视频大小建议：<100MB")

# 上传视频
uploaded_file = st.file_uploader(
    "上传视频文件",
    type=['mp4', 'mov', 'avi', 'flv', 'webm', 'mkv'],
    help="选择一个视频文件，系统将提取其中的文案"
)

if uploaded_file:
    st.success(f"✅ 已上传: {uploaded_file.name}")
    
    # 显示视频信息
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("文件名", uploaded_file.name[:20] + "...")
    with col2:
        st.metric("文件大小", f"{uploaded_file.size / 1024 / 1024:.2f} MB")
    with col3:
        st.metric("文件类型", uploaded_file.type)
    
    st.markdown("---")
    
    # 处理按钮
    if st.button("🚀 开始处理", type="primary", use_container_width=True):
        # 创建临时文件
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info("🔄 正在处理，请稍候...")
        
        try:
            # 构造输入
            video_file = File(
                url=f"file://{temp_path}",
                file_type="video"
            )
            
            graph_input = GraphInput(
                video=video_file,
                video_title=uploaded_file.name
            )
            
            # 运行工作流
            with st.spinner("🎬 正在提取视频文案..."):
                result = main_graph.invoke(graph_input)
            
            # 显示结果
            st.success("✅ 处理完成！")
            st.markdown("---")
            
            # 显示文案
            st.subheader("📝 提取的文案")
            st.text_area("", result.extracted_text, height=200, key="extracted")
            
            # 显示摘要
            st.subheader("📋 文案摘要")
            st.text_area("", result.text_summary, height=100, key="summary")
            
            # 显示分析
            st.subheader("🔍 文案分析")
            st.text_area("", result.text_analysis, height=200, key="analysis")
            
            # 显示改写
            st.subheader("✍️ 文案改写（品牌：立时）")
            st.json(result.text_rewrite)
            
            # 显示飞书链接
            if result.feishu_link:
                st.subheader("📊 飞书多维表格")
                st.markdown(f"[点击查看结果]({result.feishu_link})")
            
            # 下载结果
            st.markdown("---")
            st.subheader("💾 下载结果")
            
            result_data = {
                "视频标题": uploaded_file.name,
                "提取文案": result.extracted_text,
                "文案摘要": result.text_summary,
                "文案分析": result.text_analysis,
                "文案改写": result.text_rewrite,
                "飞书链接": result.feishu_link
            }
            
            st.download_button(
                "📥 下载结果 JSON",
                data=json.dumps(result_data, ensure_ascii=False, indent=2),
                file_name=f"{uploaded_file.name}_result.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"❌ 处理失败: {str(e)}")
            st.error("请检查视频格式和大小，或稍后重试")

# 页脚
st.markdown("---")
st.markdown("💡 技术支持：LangGraph + 豆包大模型 + 飞书多维表格")
