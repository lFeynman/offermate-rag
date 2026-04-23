from rag.pipeline import should_refuse, build_citations


def test_should_refuse_when_no_results():
    assert should_refuse([], 0.35) is True


def test_should_refuse_when_score_too_low():
    results = [{"score": 0.2}]
    assert should_refuse(results, 0.35) is True


def test_should_not_refuse_when_score_high_enough():
    results = [{"score": 0.8}]
    assert should_refuse(results, 0.35) is False


def test_build_citations():
    retrieval_results = [
        {
            "source": "data/jd/sample_jd.txt",
            "file_name": "sample_jd.txt",
            "page": None,
            "chunk_id": "c1"
        },
        {
            "source": "data/jd/sample_jd.txt",
            "file_name": "sample_jd.txt",
            "page": None,
            "chunk_id": "c2"
        }
    ]

    citations = build_citations(retrieval_results)
    assert len(citations) == 2
    assert citations[0].file_name == "sample_jd.txt"