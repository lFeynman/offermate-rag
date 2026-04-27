import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

from rag.pipeline import answer_query
from agent.workflow import run_workflow
from agent.router import route_query


st.set_page_config(page_title="OfferMate-RAG", layout="wide")

st.title("OfferMate-RAG")
st.subheader("面向岗位 JD 与技术文档的检索增强智能助手")

tab_chat, tab_match, tab_interview, tab_router = st.tabs(
    ["RAG 问答", "JD/简历匹配", "面试题生成", "Router 调试"]
)


with tab_chat:
    st.markdown("### RAG 问答")
    st.caption("该模块会调用 Qwen Embedding 和 Qwen Generation，可能消耗 token。")

    query = st.text_input("请输入你的问题", placeholder="例如：这个岗位主要要求哪些技能？")

    if st.button("开始问答"):
        if not query.strip():
            st.warning("请输入问题。")
        else:
            with st.spinner("正在检索并生成回答..."):
                result = answer_query(query, "data", top_k=3)

            st.markdown("### 回答")
            st.write(result.answer)

            st.markdown("### Grounded")
            st.write(result.grounded)

            st.markdown("### 引用")
            if result.citations:
                for c in result.citations:
                    st.write(f"- 文件：{c.file_name} | 页码：{c.page} | chunk_id：{c.chunk_id}")
            else:
                st.write("无引用")


with tab_match:
    st.markdown("### JD / 简历匹配分析")
    st.caption("该模块通过 Agent Workflow 调用规则版 tools，不调用 Qwen，不消耗 token。")

    jd_text = st.text_area("粘贴岗位 JD", height=220)
    resume_text = st.text_area("粘贴简历文本", height=220)

    if st.button("开始匹配分析"):
        if not jd_text.strip() or not resume_text.strip():
            st.warning("请同时输入岗位 JD 和简历文本。")
        else:
            jd_result = run_workflow(
                query="解析岗位要求",
                jd_text=jd_text
            )

            resume_result = run_workflow(
                query="解析简历",
                resume_text=resume_text
            )

            match_result = run_workflow(
                query="我的简历和岗位匹配吗",
                jd_text=jd_text,
                resume_text=resume_text
            )

            st.markdown("### 岗位解析结果")
            st.json(jd_result.result)

            st.markdown("### 简历解析结果")
            st.json(resume_result.result)

            st.markdown("### 匹配分析")
            if match_result.success:
                st.json(match_result.result)
            else:
                st.error(match_result.error)


with tab_interview:
    st.markdown("### 面试题生成")
    st.caption("该模块通过 Agent Workflow 调用规则版工具，不调用 Qwen，不消耗 token。")

    jd_text_q = st.text_area("粘贴岗位 JD", height=200, key="jd_for_questions")
    resume_text_q = st.text_area("粘贴简历文本", height=200, key="resume_for_questions")

    if st.button("生成面试题"):
        if not jd_text_q.strip() or not resume_text_q.strip():
            st.warning("请同时输入岗位 JD 和简历文本。")
        else:
            result = run_workflow(
                query="根据我的简历和岗位 JD 生成面试题",
                jd_text=jd_text_q,
                resume_text=resume_text_q
            )

            if not result.success:
                st.error(result.error)
            else:
                questions = result.result

                st.markdown("### 基础问题")
                for q in questions.get("basic_questions", []):
                    st.write(f"- {q}")

                st.markdown("### 技能问题")
                for q in questions.get("skill_questions", []):
                    st.write(f"- {q}")

                st.markdown("### 差距追问")
                for q in questions.get("gap_questions", []):
                    st.write(f"- {q}")

                st.markdown("### 项目问题")
                for q in questions.get("project_questions", []):
                    st.write(f"- {q}")


with tab_router:
    st.markdown("### Router 调试")
    st.caption("该模块用于查看用户请求会被路由到哪个任务。不会调用 Qwen。")

    router_query = st.text_input(
        "输入一句用户请求",
        placeholder="例如：帮我分析我的简历和这个岗位是否匹配"
    )

    if st.button("查看路由结果"):
        if not router_query.strip():
            st.warning("请输入请求。")
        else:
            route = route_query(router_query)
            st.write(f"路由结果：`{route}`")