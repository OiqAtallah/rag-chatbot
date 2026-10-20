"""Menggabungkan retriever dan LLM menjadi satu alur RAG."""

from collections.abc import Callable
from dataclasses import dataclass

from .llm import ask_llm
from .loader import load_chunks
from .retriever import Hit, TfidfRetriever

NO_CONTEXT_REPLY = "Saya tidak menemukan informasi yang relevan di dokumen."

LLMFn = Callable[[str, list[Hit]], str]


@dataclass(frozen=True)
class Answer:
    text: str
    hits: list[Hit]


class RagChatbot:
    def __init__(self, docs_dir: str, k: int = 3, llm_fn: LLMFn = ask_llm):
        self.retriever = TfidfRetriever(load_chunks(docs_dir))
        self.k = k
        self.llm_fn = llm_fn  # bisa diganti (mis. fake) untuk testing

    def retrieve(self, question: str) -> list[Hit]:
        return self.retriever.search(question, k=self.k)

    def answer(self, question: str) -> Answer:
        hits = self.retrieve(question)
        if not hits:  # tidak ada konteks relevan -> tidak perlu memanggil API
            return Answer(NO_CONTEXT_REPLY, [])
        return Answer(self.llm_fn(question, hits), hits)
