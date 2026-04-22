# OfferMate-RAG：面向岗位 JD 与技术文档的检索增强智能助手

OfferMate-RAG 是一个面向岗位 JD、简历与技术文档场景的智能求职助手项目，以 RAG（Retrieval-Augmented Generation）为核心，以 Agent Workflow 和 Tool Calling 为增强，并引入 Harness Engineering 思路，通过模块边界、Schema 约束、Prompt 模板、配置管理、测试与 CI 质量门禁，将 AI 能力收敛为可控、可复现、可交付的工程流程。

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

- 文档加载（PDF、TXT、Markdown）
- 文本切分与知识库构建
- Qwen Embedding 检索
- Qwen Generation 回答生成
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
- 基础 checks、tests 与 CI 质量门禁

---

## 3. 当前进度

### 已完成

- 项目初始化
- 基础目录结构搭建
- FastAPI 最小后端启动
- Streamlit 最小前端启动
- Agent 和 Tools 模块骨架
- Schema 约束层初版
- Prompt 模板目录初版
- Config 配置目录初版
- 文档加载模块 loader.py
- 文本切分模块 chunker.py
- load 到 chunk 的最小 pipeline
- Router 从配置文件读取路由规则
- Qwen Embedding 接入，使用 text-embedding-v4
- Qwen Generation 接入，使用 qwen-plus
- 最小 retrieval pipeline
- Router、Loader、Chunker、Pipeline 最小单元测试
- 基础 Harness Checks 占位
- GitHub Actions CI 初版

### 开发中

- 工具模块具体逻辑实现
- 引用式回答接入
- benchmark 和 regression 评测
- BM25 和 Hybrid Retrieval
- Reranker
- 更完整的端到端 workflow

---

## 4. 项目结构

    offermate-rag/
    ├── app/
    │   └── main.py
    ├── backend/
    │   └── main.py
    ├── rag/
    │   ├── loader.py
    │   ├── chunker.py
    │   ├── retriever.py
    │   ├── generator.py
    │   └── pipeline.py
    ├── agent/
    │   ├── router.py
    │   └── workflow.py
    ├── tools/
    │   ├── jd_parser.py
    │   ├── resume_parser.py
    │   ├── skill_matcher.py
    │   └── interview_generator.py
    ├── schemas/
    │   ├── common.py
    │   ├── jd.py
    │   ├── resume.py
    │   ├── match.py
    │   ├── document.py
    │   └── retrieval.py
    ├── prompts/
    │   ├── rag_answer.txt
    │   ├── router.txt
    │   ├── jd_parser.txt
    │   └── resume_parser.txt
    ├── config/
    │   ├── settings.py
    │   ├── retrieval.yaml
    │   ├── workflow.yaml
    │   └── model.yaml
    ├── harness/
    │   ├── checks/
    │   │   ├── schema_check.py
    │   │   └── route_check.py
    │   ├── eval/
    │   └── runner.py
    ├── tests/
    │   ├── unit/
    │   │   ├── test_loader.py
    │   │   ├── test_router.py
    │   │   ├── test_chunker.py
    │   │   ├── test_pipeline.py
    │   │   ├── test_retrieval_schema.py
    │   │   └── test_retriever.py
    │   └── integration/
    ├── data/
    │   ├── jd/
    │   ├── resume/
    │   ├── tech_docs/
    │   └── interview/
    ├── docs/
    ├── screenshots/
    ├── README.md
    ├── requirements.txt
    └── .gitignore

---

## 5. 技术栈

### 5.1 大模型与检索

- Qwen Embedding: text-embedding-v4
- Qwen Generation: qwen-plus
- Dense Retrieval
- Prompt Engineering
- Citation-Grounded Answering

### 5.2 Agent 与 Workflow

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

通过 rag、agent、tools、backend、app 等目录划分系统职责边界，避免功能耦合与模块混乱。

### 6.2 质量级约束

通过 schemas 固定输入输出结构，通过 prompts 管理模板，通过 tests 与 harness/checks 对关键行为进行验证。

### 6.3 流程级约束

通过 config 管理关键配置，通过 .github/workflows/ci.yml 构建基础 CI 流程，为后续持续迭代与团队协作打基础。

---

## 7. 快速开始

### 7.1 创建环境

推荐使用 Python 3.10。

    python -m venv .venv

Windows 激活：

    .venv\Scripts\activate

Linux 或 Mac 激活：

    source .venv/bin/activate

### 7.2 安装依赖

    pip install -r requirements.txt

### 7.3 配置环境变量

Windows PowerShell：

    $env:DASHSCOPE_API_KEY="你的APIKey"

Linux 或 Mac：

    export DASHSCOPE_API_KEY="你的APIKey"

### 7.4 启动后端

    uvicorn backend.main:app --reload

默认访问：

    http://127.0.0.1:8000

### 7.5 启动前端

    streamlit run app/main.py

---

## 8. 数据准备

将原始数据放入以下目录：

- data/jd/：岗位 JD
- data/resume/：简历 PDF 或 TXT
- data/tech_docs/：技术文档、学习笔记
- data/interview/：面试题、面经、八股资料

当前支持的文档类型：

- .txt
- .md
- .pdf

建议至少准备：

- 1 份岗位 JD
- 1 份简历
- 1 份技术文档
- 1 份面试题资料

---

## 9. 当前已支持的最小能力

### 9.1 文档加载

可通过 rag/loader.py 加载目录下文档，并返回统一的 text 和 metadata 结构。

### 9.2 文本切分

可通过 rag/chunker.py 将文档切分为多个 chunk，并保留：

- chunk_id
- source
- file_name
- file_type
- page（若为 PDF）

### 9.3 Qwen Embedding 检索

当前 rag/retriever.py 已支持：

- 使用 text-embedding-v4 对 query 和 chunk 编码
- 基于向量相似度返回 top-k 检索结果

### 9.4 Qwen Generation 回答

当前 rag/generator.py 已支持：

- 使用 qwen-plus
- 基于检索结果生成最小回答

### 9.5 最小 pipeline

当前 rag/pipeline.py 已支持：

- 加载文档
- 切分为 chunk
- 执行 retrieval
- 根据检索结果生成回答

### 9.6 路由配置化

agent/router.py 已支持从 config/workflow.yaml 读取路由规则，而非在代码中写死关键词。

### 9.7 基础单元测试

当前已提供最小单元测试：

- tests/unit/test_loader.py
- tests/unit/test_router.py
- tests/unit/test_chunker.py
- tests/unit/test_pipeline.py
- tests/unit/test_retrieval_schema.py
- tests/unit/test_retriever.py

运行方式：

    pytest tests/unit -v

---

## 10. 示例检查方式

### 10.1 检查检索器

    from rag.pipeline import prepare_retriever

    retriever = prepare_retriever("data", chunk_size=200, chunk_overlap=50)
    results = retriever.retrieve("这个岗位要求哪些技能", top_k=3)

    for r in results:
        print(r.model_dump())

### 10.2 检查完整问答流程

    from rag.pipeline import answer_query

    result = answer_query("这个岗位主要要求哪些技能？", "data", top_k=3)
    print(result["answer"])
    print(result["retrieval_results"][0])

### 10.3 运行单元测试

    pytest tests/unit -v

---

## 11. 后续开发计划

### 阶段一：完善工具逻辑

- 完成 JD Parser
- 完成 Resume Parser
- 完成 Skill Matcher
- 完成 Interview Question Generator

### 阶段二：补强 Harness Engineering

- 完善 checks
- 引入 benchmark 和 regression
- 完善 tests
- 扩展 CI 质量门禁

### 阶段三：增强检索效果

- 接入 BM25
- 接入 Hybrid Retrieval
- 接入 Reranker
- 输出检索评测结果

### 阶段四：增强回答质量

- 接入 citation 生成
- 优化 grounded answer
- 增加拒答策略
- 优化 end-to-end workflow

---

## 12. 项目价值

相比普通的 RAG Demo，本项目更强调：

- 场景化：围绕岗位 JD、简历与技术文档的真实求职场景设计
- 工程化：通过模块划分、Schema、配置、测试与 CI 提高可维护性
- 可控性：通过 Harness Engineering 思路约束 AI 输出行为
- 可展示性：兼具 GitHub 项目展示、简历项目描述与面试讲解价值

---

## 13. License

当前仅用于个人学习、项目展示与求职场景实践，后续可根据需要补充正式 License。
