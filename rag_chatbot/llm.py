"""Pemanggilan LLM (Claude API) dan penyusunan prompt."""

import os

from .retriever import Hit

DEFAULT_MODEL = "claude-sonnet-5-5"

SYSTEM_PROMPT = (
    "Kamu asisten tanya-jawab dokumen. Jawab dalam bahasa Indonesia, singkat dan jelas, "
    "HANYA berdasarkan konteks yang diberikan. Jika konteks tidak memuat jawabannya, "
    "katakan bahwa kamu tidak menemukan jawabannya di dokumen. "
    "Sebutkan sumber memakai format [nama_file#nomor_chunk]."
)


def build_prompt(question: str, hits: list[Hit]) -> str:
    context = "\n\n".join(f"[{h.chunk.source}#{h.chunk.index}]\n{h.chunk.text}" for h in hits)
    return f"<konteks>\n{context}\n</konteks>\n\nPertanyaan: {question}"


def ask_llm(question: str, hits: list[Hit], model: str | None = None, max_tokens: int = 500) -> str:
    """Kirim pertanyaan + konteks ke Claude. Membutuhkan ANTHROPIC_API_KEY."""
    import anthropic  # di-import di sini agar test/dry-run tidak butuh API key

    client = anthropic.Anthropic()  # membaca ANTHROPIC_API_KEY dari environment
    response = client.messages.create(
        model=model or os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL),
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(question, hits)}],
    )
    return "".join(block.text for block in response.content if block.type == "text")
