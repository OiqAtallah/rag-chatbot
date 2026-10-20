import pytest

from rag_chatbot.loader import load_chunks, split_text


def test_split_text_overlap():
    text = " ".join(str(i) for i in range(10))
    chunks = split_text(text, chunk_size=4, overlap=2)
    assert chunks[0] == "0 1 2 3"
    assert chunks[1] == "2 3 4 5"
    assert chunks[-1].endswith("9")


def test_split_text_short_text_single_chunk():
    assert split_text("halo dunia", chunk_size=10, overlap=2) == ["halo dunia"]


def test_split_text_empty():
    assert split_text("   ") == []


@pytest.mark.parametrize("size,overlap", [(0, 0), (5, 5), (5, -1)])
def test_split_text_invalid_args(size, overlap):
    with pytest.raises(ValueError):
        split_text("a b c", chunk_size=size, overlap=overlap)


def test_load_chunks_reads_sample_docs():
    chunks = load_chunks("data/docs")
    assert {c.source for c in chunks} >= {"metrik_bisnis.md", "sql_dasar.md", "kualitas_data.md"}


def test_load_chunks_empty_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_chunks(tmp_path)
