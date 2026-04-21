# OfferMate-RAG：面向岗位 JD 与技术文档的检索增强智能助手

OfferMate-RAG 是一个面向岗位 JD、简历与技术文档场景的智能求职助手项目，以 **RAG（Retrieval-Augmented Generation）** 为核心，以 **Agent Workflow + Tool Calling** 为增强，并引入 **Harness Engineering** 思路，通过模块边界、Schema 约束、Prompt 模板、配置管理、测试与 CI 质量门禁，将 AI 能力收敛为可控、可复现、可交付的工程流程。

---

## 1. 项目目标

本项目旨在构建一个面向求职场景的检索增强智能助手，支持以下能力：

- 基于岗位 JD、简历与技术文档进行问答
- 输出带引用的可信回答
- 对用户请求进行任务路由，并调用对应工具模块
- 解析岗位要求与简历内容，完成技能匹配分析
- 生成针对性的面试问题
- 通过约束体系降低 AI 输出的不确定性，提升工程可控性

---

## 2. 核心特性

### 2.1 RAG 主链路
- 文档加载（PDF / TXT / Markdown）
- 文本切分与知识库构建
- 检索增强问答
- 引用式回答
- 无依据拒答

### 2.2 Agent Workflow
- 基于任务意图的路由机制
- 按需调用工具模块
- 支持 RAG、JD 解析、简历解析、技能匹配、面试题生成等不同任务路径
- 路由规则通过配置文件管理，避免逻辑硬编码

### 2.3 Tool Calling
- JD Parser
- Resume Parser
- Skill Matcher
- Interview Question Generator

### 2.4 Harness Engineering
- 模块边界清晰划分
- 统一 Schema 约束输入输出
- Prompt 模板外置管理
- 配置中心统一管理系统行为
- 基础 checks / tests / CI 质量门禁

---

## 3. 当前进度

### 已完成
- [x] 项目初始化
- [x] 基础目录结构搭建
- [x] FastAPI 最小后端启动
- [x] Streamlit 最小前端启动
- [x] Agent / Tools 模块骨架
- [x] Schema 约束层初版
- [x] Prompt 模板目录初版
- [x] Config 配置目录初版
- [x] 文档加载模块 `loader.py`
- [x] 文本切分模块 `chunker.py`
- [x] `load -> chunk` 最小 pipeline
- [x] Router 从配置文件读取路由规则
- [x] Router / Loader / Chunker / Pipeline 最小单元测试
- [x] 基础 Harness Checks 占位
- [x] GitHub Actions CI 初版

### 开发中
- [ ] 检索模块 `retriever.py`
- [ ] 回答生成模块 `generator.py`
- [ ] RAG 主流程 `pipeline.py` 扩展
- [ ] 工具模块具体逻辑实现
- [ ] 引用式回答接入
- [ ] benchmark / regression 评测
- [ ] BM25 / Hybrid Retrieval
- [ ] Reranker

---

## 4. 项目结构

```text
offermate-rag/
├── app/                          # 前端展示层（Streamlit）
│   └── main.py
├── backend/                      # API 层（FastAPI）
│   └── main.py
├── rag/                          # RAG 主链路
│   ├── loader.py                 # 文档加载
│   ├── chunker.py                # 文本切分
│   ├── retriever.py              # 检索（待完善）
│   ├── generator.py              # 回答生成（待完善）
│   └── pipeline.py               # 当前支持 load -> chunk 最小流程
├── agent/                        # Agent 路由与流程编排
│   ├── router.py                 # 已支持从 workflow.yaml 读取规则
│   └── workflow.py
├── tools/                        # 可被 agent 调用的工具模块
│   ├── jd_parser.py
│   ├── resume_parser.py
│   ├── skill_matcher.py
│   └── interview_generator.py
├── schemas/                      # 统一输入输出约束
│   ├── common.py
│   ├── jd.py
│   ├── resume.py
│   ├── match.py
│   └── document.py               # 文档 chunk schema
├── prompts/                      # Prompt 模板管理
│   ├── rag_answer.txt
│   ├── router.txt
│   ├── jd_parser.txt
│   └── resume_parser.txt
├── config/                       # 配置中心
│   ├── settings.py
│   ├── retrieval.yaml
│   └── workflow.yaml
├── harness/                      # Harness Engineering 相关检查与验证
│   ├── checks/
│   │   ├── schema_check.py
│   │   └── route_check.py
│   ├── eval/
│   └── runner.py
├── tests/                        # 测试层
│   ├── unit/
│   │   ├── test_loader.py
│   │   ├── test_router.py
│   │   ├── test_chunker.py
│   │   └── test_pipeline.py
│   └── integration/
├── data/                         # 原始输入数据
│   ├── jd/
│   ├── resume/
│   ├── tech_docs/
│   └── interview/
├── docs/
├── screenshots/
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 5. 技术栈

### 5.1 大模型 / RAG
- Retrieval-Augmented Generation (RAG)
- Dense Retrieval
- BM25（计划接入）
- Reranker（计划接入）
- Prompt Engineering
- Citation-Grounded Answering

### 5.2 Agent / Workflow
- Intent Routing
- Tool Calling
- Config-Driven Routing
- Multi-step Workflow

### 5.3 后端与前端
- Python
- FastAPI
- Streamlit

### 5.4 工程与质量
- Pydantic
- PyTest
- Git / GitHub
- GitHub Actions CI
- YAML Config

### 5.5 文档处理
- PyMuPDF
- TXT / Markdown / PDF 文档加载

---

## 6. Harness Engineering 设计思路

本项目不仅关注 AI 功能本身，也关注 AI 系统的可控性与可交付性。为此，项目引入 Harness Engineering 思路，通过三层约束降低模型输出的不确定性。

### 6.1 架构级约束
通过 `rag/`、`agent/`、`tools/`、`backend/`、`app/` 等目录划分系统职责边界，避免功能耦合与模块混乱。

### 6.2 质量级约束
通过 `schemas/` 固定输入输出结构，通过 `prompts/` 管理模板，通过 `tests/` 与 `harness/checks/` 对关键行为进行验证。

### 6.3 流程级约束
通过 `config/` 管理关键配置，通过 `.github/workflows/ci.yml` 构建基础 CI 流程，为后续持续迭代与团队协作打基础。

---

## 7. 快速开始

### 7.1 创建环境

推荐使用 Python 3.10。

```bash
python -m venv .venv
```

Windows 激活：

```powershell
.venv\Scripts\activate
```

Linux / Mac 激活：

```bash
source .venv/bin/activate
```

### 7.2 安装依赖

```bash
pip install -r requirements.txt
```

### 7.3 启动后端

```bash
uvicorn backend.main:app --reload
```

默认访问：

```text
http://127.0.0.1:8000
```

### 7.4 启动前端

```bash
streamlit run app/main.py
```

---

## 8. 数据准备

将原始数据放入以下目录：

- `data/jd/`：岗位 JD
- `data/resume/`：简历 PDF / TXT
- `data/tech_docs/`：技术文档、学习笔记
- `data/interview/`：面试题、面经、八股资料

当前支持的文档类型：

- `.txt`
- `.md`
- `.pdf`

建议至少准备：

- 1 份岗位 JD
- 1 份简历
- 1 份技术文档
- 1 份面试题资料

---

## 9. 当前已支持的最小能力

### 9.1 文档加载
可通过 `rag/loader.py` 加载目录下文档，并返回统一的 `text + metadata` 结构。

### 9.2 文本切分
可通过 `rag/chunker.py` 将文档切分为多个 chunk，并保留：

- `chunk_id`
- `source`
- `file_name`
- `file_type`
- `page`（若为 PDF）

### 9.3 最小 pipeline
当前 `rag/pipeline.py` 已支持：

- 加载文档
- 切分为 chunk
- 输出结构化 chunk 列表

### 9.4 路由配置化
`agent/router.py` 已支持从 `config/workflow.yaml` 读取路由规则，而非在代码中写死关键词。

### 9.5 基础单元测试
当前已提供最小单元测试：

- `tests/unit/test_loader.py`
- `tests/unit/test_router.py`
- `tests/unit/test_chunker.py`
- `tests/unit/test_pipeline.py`

运行方式：

```bash
pytest tests/unit -v
```

---

## 10. 示例检查方式

### 10.1 检查文档加载

```python
from rag.loader import load_documents

docs = load_documents("data")
print(len(docs))
print(docs[0]["metadata"])
```

### 10.2 检查文档切分

```python
from rag.loader import load_documents
from rag.chunker import chunk_documents

docs = load_documents("data")
chunks = chunk_documents(docs, chunk_size=200, chunk_overlap=50)
print(len(chunks))
print(chunks[0].model_dump())
```

### 10.3 检查最小 pipeline

```python
from rag.pipeline import prepare_chunks

chunks = prepare_chunks("data", chunk_size=200, chunk_overlap=50)
print(len(chunks))
print(chunks[0].model_dump())
```

### 10.4 检查路由

```python
from agent.router import route_query

print(route_query("这个岗位要求哪些技能"))
print(route_query("帮我分析我的简历"))
print(route_query("我的简历和岗位匹配吗"))
print(route_query("给我生成一些面试题"))
print(route_query("这篇技术文档主要讲什么"))
```

---

## 11. 后续开发计划

### 阶段一：完成 RAG 主链路
- 完成 `retriever.py`
- 完成 `generator.py`
- 扩展 `pipeline.py`
- 接入引用式回答

### 阶段二：完成工具逻辑
- 完成 JD Parser
- 完成 Resume Parser
- 完成 Skill Matcher
- 完成 Interview Question Generator

### 阶段三：补强 Harness Engineering
- 完善 checks
- 引入 benchmark / regression
- 完善 tests
- 扩展 CI 质量门禁

### 阶段四：增强检索效果
- 接入 BM25
- 接入 Hybrid Retrieval
- 接入 Reranker
- 输出检索评测结果

---

## 12. 项目价值

相比普通的 RAG Demo，本项目更强调：

- 场景化：围绕岗位 JD、简历与技术文档的真实求职场景设计
- 工程化：通过模块划分、Schema、配置、测试与 CI 提高可维护性
- 可控性：通过 Harness Engineering 思路约束 AI 输出行为

---

## 13. License

当前仅用于个人学习、项目展示与求职场景实践，后续可根据需要补充正式 License。