from typing import List, Dict
from schemas.document import DocumentChunk


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    if chunk_size <= chunk_overlap:
        raise ValueError("chunk_size must be larger than chunk_overlap")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)

        if end == text_length:
            break

        start = end - chunk_overlap

    return chunks


def chunk_document(doc: Dict, chunk_size: int = 500, chunk_overlap: int = 100) -> List[DocumentChunk]:
    chunks = []

    metadata = doc.get("metadata", {})
    source = metadata.get("source", "")
    file_name = metadata.get("file_name", "")
    file_type = metadata.get("file_type", "")

    # PDF 按页切分后再 chunk
    if file_type == "pdf" and "pages" in doc:
        for page_info in doc["pages"]:
            page_num = page_info["page"]
            page_text = page_info["text"]

            sub_chunks = split_text(page_text, chunk_size, chunk_overlap)
            for idx, chunk_text in enumerate(sub_chunks):
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{file_name}_p{page_num}_c{idx}",
                        text=chunk_text,
                        source=source,
                        file_name=file_name,
                        file_type=file_type,
                        page=page_num,
                        extra_metadata={}
                    )
                )
    else:
        text = doc.get("text", "")
        sub_chunks = split_text(text, chunk_size, chunk_overlap)

        for idx, chunk_text in enumerate(sub_chunks):
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{file_name}_c{idx}",
                    text=chunk_text,
                    source=source,
                    file_name=file_name,
                    file_type=file_type,
                    page=None,
                    extra_metadata={}
                )
            )

    return chunks


def chunk_documents(docs: List[Dict], chunk_size: int = 500, chunk_overlap: int = 100) -> List[DocumentChunk]:
    all_chunks = []

    for doc in docs:
        doc_chunks = chunk_document(doc, chunk_size, chunk_overlap)
        all_chunks.extend(doc_chunks)

    return all_chunks