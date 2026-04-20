from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
# 原始数据目录，放 JD、简历、技术文档等输入文件
DATA_DIR = BASE_DIR / "data"
# 提示词目录，保存给 RAG、Agent 等模块复用的 prompt
PROMPT_DIR = BASE_DIR / "prompts"