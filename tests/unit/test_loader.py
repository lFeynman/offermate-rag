from rag.loader import load_file


# 验证 txt 文件可被正确加载，并返回统一结构。
def test_load_txt(tmp_path):
    # tmp_path 是 pytest 提供的临时目录，不污染仓库文件。
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world", encoding="utf-8")

    result = load_file(str(file_path))
    # 断言读取到的正文与写入内容一致。
    assert result["text"] == "hello world"
    # 断言 metadata 中的文件类型识别正确。
    assert result["metadata"]["file_type"] == "txt"