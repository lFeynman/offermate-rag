import streamlit as st

st.set_page_config(page_title="OfferMate-RAG", layout="wide")

st.title("OfferMate-RAG")
st.subheader("面向岗位 JD 与技术文档的检索增强智能助手")

st.markdown("### 当前状态")
st.info("Day 1：项目初始化完成，后续将接入 RAG、Agent Router、Tools 与评测模块。")

st.markdown("### 计划功能")
st.write("- 文档解析")
st.write("- 检索增强问答")
st.write("- Agent 路由")
st.write("- JD / 简历解析")
st.write("- 技能匹配分析")
st.write("- 面试题生成")