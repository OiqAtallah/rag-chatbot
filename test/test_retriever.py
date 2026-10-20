import pytest

from rag_chatbot.loader import load_chunks
from rag_chatbot.retriever import TfidfRetriever


@pytest.fixture(scope="module")
def retriever():
    return TfidfRetriever(load_chunks("data/docs"))


@pytest.mark.parametrize(
    "question,expected_source",
    [
        ("Apa itu churn rate?", "metrik_bisnis.md"),
        ("Apa bedanya INNER JOIN dan LEFT JOIN?", "sql_dasar.md"),
        ("Bagaimana mendeteksi outlier dengan IQR?", "kualitas_data.md"),
    ],
)
def test_top_hit_is_expected_source(retriever, question, expected_source):
    hits = retriever.search(question, k=3)
    assert hits and hits[0].chunk.source == expected_source


def test_irrelevant_query_returns_nothing(retriever):
    assert retriever.search("resep nasi goreng kampung", k=3) == []


def test_empty_chunks_rejected():
    with pytest.raises(ValueError):
        TfidfRetriever([])
