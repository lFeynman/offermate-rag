# OfferMate-RAG：面向岗位 JD 与技术文档的检索增强智能助手

OfferMate-RAG 是一个以 RAG 为核心、以 tool use 为增强的场景化求职助手，支持岗位 JD、简历与技术文档的解析、检索问答、技能匹配分析与面试问题生成。

## 项目目标
本项目希望构建一个可落地的求职场景智能助手，具备以下能力：

- 基于岗位 JD、简历与技术文档进行问答
- 输出带引用的可信回答
- 通过任务路由调用不同工具模块
- 分析岗位与简历的技能匹配情况
- 生成针对性的面试问题

## 核心模块
- `rag/`：文档加载、chunk 切分、检索、生成、主链路
- `agent/`：任务路由与工作流
- `tools/`：JD Parser、Resume Parser、Skill Matcher、Interview Question Generator
- `eval/`：benchmark 与评测脚本
- `app/`：前端界面
- `backend/`：FastAPI 后端

## 当前进度
- [x] 项目初始化
- [x] 目录结构搭建
- [x] 最小前后端启动
- [x] Agent / Tools 模块占位
- [ ] 文档解析
- [ ] RAG 检索问答
- [ ] 引用式回答
- [ ] 工具调用
- [ ] 评测模块

## 目录结构
```text
offermate-rag/
├── app/
├── backend/
├── rag/
├── agent/
├── tools/
├── eval/
├── data/
└── screenshots/

## 启动方式
pip install -r requirements.txt
uvicorn backend.main:app --reload
streamlit run app/main.py