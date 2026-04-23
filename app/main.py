import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from rag.pipeline import answer_query
st.set_page_config(page_title="OfferMate-RAG", layout="wide")

st.title("OfferMate-RAG")
st.subheader("面向岗位 JD 与技术文档的检索增强智能助手")

query = st.text_input("请输入你的问题", placeholder="例如：这个岗位主要要求哪些技能？")

if st.button("开始问答"):
    if not query.strip():
        st.warning("请输入问题。")
    else:
        with st.spinner("正在检索并生成回答..."):
            result = answer_query(query, "data", top_k=3)

        st.markdown("### 回答")
        st.write(result.answer)

        st.markdown("### grounded")
        st.write(result.grounded)

        st.markdown("### 引用")
        if result.citations:
            for c in result.citations:
                st.write(f"- 文件：{c.file_name} | 页码：{c.page} | chunk_id：{c.chunk_id}")
        else:
            st.write("无引用")