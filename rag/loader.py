from pathlib import Path
from typing import List, Dict
import fitz


# 读取纯文本文件，并统一包装成 "text + metadata" 结构
def load_txt(file_path: Path) -> Dict:
    text = file_path.read_text(encoding="utf-8")
    return {
        "text": text,
        "metadata": {
            "source": str(file_path),
            "file_name": file_path.name,
            "file_type": "txt"
        }
    }


# 读取 Markdown 文件
def load_md(file_path: Path) -> Dict:
    text = file_path.read_text(encoding="utf-8")
    return {
        "text": text,
        "metadata": {
            "source": str(file_path),
            "file_name": file_path.name,
            "file_type": "md"
        }
    }


# 读取 PDF：既保留整篇文本，也保留逐页文本，便于后续做页级引用
def load_pdf(file_path: Path) -> Dict:
    doc = fitz.open(file_path)
    pages = []
    full_text = []

    # 枚举每一页并提取文本，页码从 1 开始，便于和阅读器显示一致
    for i, page in enumerate(doc):
        page_text = page.get_text()
        pages.append({
            "page": i + 1,
            "text": page_text
        })
        full_text.append(page_text)

    return {
        "text": "\n".join(full_text),
        "pages": pages,
        "metadata": {
            "source": str(file_path),
            "file_name": file_path.name,
            "file_type": "pdf"
        }
    }


# 根据文件后缀分发到对应 loader，作为统一入口给上层调用
def load_file(file_path: str) -> Dict:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return load_txt(path)
    elif suffix == ".md":
        return load_md(path)
    elif suffix == ".pdf":
        return load_pdf(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


# 扫描目录下所有支持格式文件，逐个加载并汇总
def load_documents(data_dir: str) -> List[Dict]:
    path = Path(data_dir)
    docs = []

    for file_path in path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".txt", ".md", ".pdf"]:
            try:
                docs.append(load_file(str(file_path)))
            except Exception as e:
                print(f"Failed to load {file_path}: {e}")

    return docs