from rag_chatbot.chatbot import NO_CONTEXT_REPLY, RagChatbot
from rag_chatbot.llm import build_prompt


def test_answer_uses_llm_with_retrieved_context():
    calls = []

    def fake_llm(question, hits):
        calls.append((question, hits))
        return "jawaban palsu"

    bot = RagChatbot("data/docs", llm_fn=fake_llm)
    result = bot.answer("Apa itu churn rate?")

    assert result.text == "jawaban palsu"
    assert len(calls) == 1
    assert result.hits[0].chunk.source == "metrik_bisnis.md"


def test_no_context_skips_llm():
    def boom(question, hits):
        raise AssertionError("LLM tidak boleh dipanggil")

    bot = RagChatbot("data/docs", llm_fn=boom)
    result = bot.answer("resep nasi goreng kampung")
    assert result.text == NO_CONTEXT_REPLY
    assert result.hits == []


def test_build_prompt_contains_question_and_source():
    bot = RagChatbot("data/docs", llm_fn=lambda q, h: "")
    hits = bot.retrieve("Apa itu churn rate?")
    prompt = build_prompt("Apa itu churn rate?", hits)
    assert "Apa itu churn rate?" in prompt
    assert "[metrik_bisnis.md#0]" in prompt
