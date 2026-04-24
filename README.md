## 1. 项目目标

本项目旨在构建一个面向求职场景的检索增强智能助手，支持以下能力：

- 基于岗位 JD、简历与技术文档进行问答
- 输出带引用的可信回答
- 对用户请求进行任务路由，并调用对应工具模块
- 解析岗位要求与简历内容，完成技能匹配分析
- 生成针对性的面试问题
- 通过工程约束体系降低 AI 输出的不确定性，提升系统可控性与可维护性

---

## 2. 核心特性

### 2.1 RAG 主链路

- 文档加载（PDF / TXT / Markdown）
- 文本切分与知识库构建
- Qwen Embedding 检索
- Qwen Generation 回答生成
- 引用式回答
- 基础拒答机制

### 2.2 Agent Workflow

- 基于任务意图的路由机制
- 支持通过配置文件管理路由规则
- 当前已支持 **priority-based router**
- 可避免“简历”“匹配”等多个关键词同时命中时的错误路由
- 后续计划升级为 scoring router 与 LLM fallback router

### 2.3 Tool Calling

当前项目保留以下工具模块结构：

- JD Parser
- Resume Parser
- Skill Matcher
- Interview Question Generator

当前阶段的重点是先完成稳定的路由与工程约束框架，后续将逐步完善工具模块的具体逻辑。

### 2.4 Harness Engineering

本项目不仅关注 AI 功能本身，也关注 AI 系统的稳定交付。当前通过以下方式体现 Harness Engineering 思路：

- 模块边界清晰划分
- 统一 Schema 约束输入输出
- Prompt 模板外置管理
- Config 配置中心统一管理系统行为
- Router 规则配置化
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
- [x] Qwen Embedding 接入（`text-embedding-v4`）
- [x] Qwen Generation 接入（`qwen-plus`）
- [x] 最小 retrieval pipeline
- [x] 回答结构化输出（`RAGResponse` / `Citation`）
- [x] 基础拒答机制（score threshold）
- [x] 引用构建逻辑
- [x] 最小 `/chat` API
- [x] Streamlit 问答演示页
- [x] Router 从配置文件读取路由规则
- [x] Priority-based router：解决多关键词同时命中时的路由优先级问题
- [x] Router / Loader / Chunker / Pipeline / Answer Logic 最小单元测试
- [x] 基础 Harness Checks 占位
- [x] GitHub Actions CI 初版

### 当前重点

- [x] 将 router 从简单关键词命中升级为优先级路由
- [ ] 完善工具模块的具体逻辑
- [ ] 优化面试题生成质量
- [ ] 引入更稳定的 task scoring 机制
- [ ] 构建更完整的 Agent Workflow

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
│   ├── retriever.py              # Qwen embedding 检索
│   ├── generator.py              # Qwen generation 回答生成
│   └── pipeline.py               # retrieval -> answer 主流程
├── agent/                        # Agent 路由与流程编排
│   ├── router.py                 # priority-based router
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
│   ├── document.py
│   └── retrieval.py
├── prompts/                      # Prompt 模板管理
│   ├── rag_answer.txt
│   ├── router.txt
│   ├── jd_parser.txt
│   └── resume_parser.txt
├── config/                       # 配置中心
│   ├── settings.py
│   ├── retrieval.yaml
│   ├── workflow.yaml             # router keywords + priority
│   ├── model.yaml
│   └── answer.yaml
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
│   │   ├── test_pipeline.py
│   │   ├── test_retrieval_schema.py
│   │   ├── test_retriever.py
│   │   ├── test_answer_logic.py
│   │   └── test_chat_response_schema.py
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

- Qwen Embedding：`text-embedding-v4`
- Qwen Generation：`qwen-plus`
- Dense Retrieval
- Prompt Engineering
- Citation-Grounded Answering

### 5.2 Agent / Workflow

- Intent Routing
- Priority-based Routing
- Tool Calling
- Config-Driven Routing
- Multi-step Workflow（开发中）

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

## 6. Priority-based Router 设计

在早期版本中，router 采用简单关键词命中方式。该方式存在一个问题：当用户请求同时包含多个关键词时，可能被路由到错误模块。

例如：

> 帮我分析我的简历和这个岗位是否匹配

这句话同时包含“简历”“匹配”“岗位”，如果仅按关键词顺序匹配，可能会错误进入 `resume_parser`。真实意图通常应为 `skill_matcher`。

因此，当前版本引入 priority-based router，在 `config/workflow.yaml` 中为不同 route 设置优先级。当前优先级如下：

- `skill_matcher`：100
- `interview_generator`：90
- `jd_parser`：70
- `resume_parser`：60

这样可以保证组合型任务优先于单文档解析任务。

---

## 7. Harness Engineering 设计思路

本项目不仅关注 AI 功能本身，也关注 AI 系统的可控性与可交付性。为此，项目引入 Harness Engineering 思路，通过三层约束降低模型输出的不确定性。

### 7.1 架构级约束

通过 `rag/`、`agent/`、`tools/`、`backend/`、`app/` 等目录划分系统职责边界，避免功能耦合与模块混乱。

### 7.2 质量级约束

通过 `schemas/` 固定输入输出结构，通过 `prompts/` 管理模板，通过 `tests/` 与 `harness/checks/` 对关键行为进行验证。

### 7.3 流程级约束

通过 `config/` 管理关键配置，通过 `.github/workflows/ci.yml` 构建基础 CI 流程，为后续持续迭代与团队协作打基础。

当前 router 的 priority 机制也是流程级约束的一部分：它通过配置文件显式规定任务路由优先级，避免多意图输入下出现不稳定行为。

---

## 8. 快速开始

### 8.1 创建环境

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

### 8.2 安装依赖

```bash
pip install -r requirements.txt
```

### 8.3 配置环境变量

Windows PowerShell：

```powershell
$env:DASHSCOPE_API_KEY="你的APIKey"
```

Linux / Mac：

```bash
export DASHSCOPE_API_KEY="你的APIKey"
```

### 8.4 启动前端

```bash
streamlit run app/main.py
```

### 8.5 启动后端（可选）

```bash
uvicorn backend.main:app --reload
```

默认访问：`http://127.0.0.1:8000`

---

## 9. 数据准备

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

## 10. RAG 具体实现流程（按代码执行顺序）

下面按一次完整问答请求的真实执行顺序，梳理当前项目中的 RAG 实现，并列出每个阶段使用的方法。

### 10.1 请求入口与主流程调度

- 入口方法：`backend/main.py` 中 `chat(req: ChatRequest)`
- 核心调用：`rag/pipeline.py` 中 `answer_query(query, data_dir, top_k)`
- 作用：接收用户问题与数据目录，进入统一 RAG 主流程。

### 10.2 文档加载（Load）

- 主入口方法：`load_documents(data_dir)`
- 文件分发方法：`load_file(file_path)`
- 按类型加载方法：
	- `load_txt(file_path)`
	- `load_md(file_path)`
	- `load_pdf(file_path)`
- 关键实现点：
	- 使用 `Path.rglob("*")` 扫描目录。
	- 仅接收 `.txt/.md/.pdf`。
	- PDF 在 `load_pdf` 中按页提取，保存 `pages`（含页码与页文本），为后续页级引用做准备。
	- 输出统一为 `text + metadata` 结构（`source/file_name/file_type`）。

### 10.3 文本切分（Chunk）

- 切分基础方法：`split_text(text, chunk_size, chunk_overlap)`
- 单文档切分方法：`chunk_document(doc, chunk_size, chunk_overlap)`
- 批量切分方法：`chunk_documents(docs, chunk_size, chunk_overlap)`
- 结构化载体：`schemas/document.py` 中 `DocumentChunk`
- 关键实现点：
	- 滑窗切分策略：`start -> end`，下一段从 `end - chunk_overlap` 开始。
	- 参数约束：`chunk_size` 必须大于 `chunk_overlap`。
	- PDF 先按页再切块，`chunk_id` 采用 `文件名_p页码_c块序号`；非 PDF 采用 `文件名_c块序号`。

### 10.4 向量化与索引构建（Embed + Index）

- 流程方法：
	- `prepare_chunks(data_dir, chunk_size, chunk_overlap)`
	- `prepare_retriever(data_dir, chunk_size, chunk_overlap)`
- 检索器类：`QwenDenseRetriever`
- 检索器核心方法：
	- `__init__()`：加载配置与初始化 OpenAI 兼容客户端
	- `_embed_texts(texts)`：调用 embedding 接口批量向量化
	- `_normalize(vectors)`：向量归一化
	- `build_index(chunks)`：为全部 chunk 建立内存索引
- 关键实现点：
	- 配置来源：`config/retrieval.yaml` 与 `config/model.yaml`。
	- Embedding 模型：`text-embedding-v4`。
	- 维度参数：`embedding_dimensions=1024`。
	- 批处理参数：`batch_size`。
	- 相似度准备：`normalize_embeddings=true` 时做 L2 归一化。

### 10.5 相似度检索（Retrieve）

- 检索方法：`QwenDenseRetriever.retrieve(query, top_k)`
- 结果结构：`schemas/retrieval.py` 中 `RetrievalResult`
- 关键实现点：
	- 对 query 向量化后，与 chunk 向量做点积：`scores = np.dot(...)`。
	- 使用 `np.argsort(scores)[::-1][:k]` 选取 Top-K。
	- 返回字段包含 `chunk_id/text/score/source/file_name/file_type/page`。

### 10.6 证据门控与拒答（Refuse Gate）

- 判定方法：`should_refuse(retrieval_results, min_score_threshold)`
- 配置来源：`config/answer.yaml`
- 关键实现点：
	- 无检索结果时直接拒答。
	- 若 `top_score < min_score_threshold` 则拒答。
	- 拒答返回使用 `refuse_message`，并标记：
		- `grounded = False`
		- `citations = []`

### 10.7 上下文构建与答案生成（Generate）

- 生成器类：`QwenGenerator`
- 生成器核心方法：
	- `__init__()`：加载模型配置与系统提示词
	- `generate(query, contexts)`：拼接上下文并调用对话模型
- 关键实现点：
	- 提示词模板来自 `prompts/rag_answer.txt`。
	- 生成模型来自 `config/model.yaml` 的 `qwen-plus`。
	- `answer_query` 中按 `max_context_items` 截断上下文，避免引入过多低相关内容。

### 10.8 引用构建与结构化输出（Citation + Response）

- 引用构建方法：`build_citations(retrieval_results)`
- 输出结构：`schemas/common.py` 中 `Citation` 与 `RAGResponse`
- API 输出：`result.model_dump()`
- 关键实现点：
	- 通过 `(source, file_name, page, chunk_id)` 去重引用。
	- 最终返回三要素：`answer`、`citations`、`grounded`。

### 10.9 一次完整调用链总结

`chat -> answer_query -> prepare_retriever -> load_documents -> chunk_documents -> build_index -> retrieve -> should_refuse -> (generate + build_citations) -> RAGResponse`

这条链路已经覆盖当前项目的最小可用 RAG 闭环：从多源文档读取、切分、向量检索、证据门控、生成回答到引用化输出。

---

## 11. 示例检查方式

### 11.1 检查完整问答流程

```python
from rag.pipeline import answer_query

result = answer_query("这个岗位主要要求哪些技能？", "data", top_k=3)
print(result.model_dump())
```

注意：该流程会调用 Qwen Embedding 与 Qwen Generation，会消耗 token。

### 11.2 检查拒答逻辑

```python
from rag.pipeline import answer_query

result = answer_query("今天天气怎么样？", "data", top_k=3)
print(result.model_dump())
```

注意：该流程会调用 Qwen Embedding；若未触发拒答，还会调用 Qwen Generation。

### 11.3 检查 router

```python
from agent.router import route_query

print(route_query("帮我分析我的简历和这个岗位是否匹配"))
print(route_query("根据我的简历和岗位 JD 生成面试题"))
print(route_query("帮我解析这份简历"))
```

该检查不调用 Qwen，不消耗 token。

### 11.4 运行单元测试

```bash
pytest tests/unit -v
```

---

## 12. 当前限制与后续优化

### 12.1 Router 仍是规则版

当前 router 已升级为 priority-based router，但本质仍属于规则路由。

当前优点：

- 稳定
- 可测试
- 不消耗 token
- 行为可控

当前限制：

- 对复杂表达的泛化能力有限
- 对多意图任务仍是 priority 粗粒度处理
- 无法主动判断用户信息是否缺失

后续计划：

- Scoring Router：在 priority 基础上加入关键词命中数量、任务类型权重等得分机制。
- Rule Router + LLM Router Fallback：规则置信度较低时再调用 Qwen 进行意图判断。
- Multi-step Planner：对复杂任务进行拆解（先解析 JD，再解析简历，再做匹配与建议生成）。

### 12.2 面试题生成仍需优化

当前项目已保留 Interview Question Generator 模块，但后续仍需增强问题质量。

当前问题：

- 固定模板生成的问题较机械
- 对不同岗位的针对性不足
- 对简历项目的深挖不够
- 缺少基于短板的自然追问

后续计划：

- 问题类型分层：基础问题、技术问题、项目深挖、差距追问、行为面问题。
- 技术题库增强：围绕 RAG、Embedding、BM25、Reranker、FastAPI、Agent、Docker 等维护模板。
- 基于匹配结果生成追问：根据 missing skills 自动生成差距追问。
- Qwen-based Interview Generator：结合 JD 解析、简历解析与技能匹配结果生成更自然问题。

### 12.3 Tool 模块仍需完善

`tools/` 目录已建立，但 JD Parser、Resume Parser、Skill Matcher、Interview Generator 仍有提升空间。

后续目标：

- 提升 JD 技能抽取准确率
- 提升简历项目与技能解析质量
- 引入结构化输出校验
- 增加工具模块单元测试
- 将工具结果更紧密接入 Agent Workflow

---

## 13. 后续开发计划

### 阶段一：完善工具逻辑

- 完成 JD Parser
- 完成 Resume Parser
- 完成 Skill Matcher
- 完成 Interview Question Generator

### 阶段二：优化 Agent Workflow

- 完善 priority router
- 引入 scoring router
- 增加 LLM fallback router
- 支持多步任务编排

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

### 阶段五：增强回答质量

- 优化 citation 展示
- 优化 grounded answer
- 增强拒答策略
- 完善端到端 workflow

---

## 14. 项目价值

相比普通的 RAG Demo，本项目更强调：

- 场景化：围绕岗位 JD、简历与技术文档的真实求职场景设计
- 工程化：通过模块划分、Schema、配置、测试与 CI 提高可维护性
- 可控性：通过 Harness Engineering 思路约束 AI 输出行为
- 可扩展性：通过 Agent Router 与 Tools 结构支持后续多任务扩展
- 可展示性：兼具 GitHub 项目展示、简历项目描述与面试讲解价值

---

## 15. License

当前仅用于个人学习、项目展示与求职场景实践，后续可根据需要补充正式 License。