"""Memuat dokumen teks dan memecahnya menjadi chunk."""

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_SUFFIXES = {".md", ".txt"}


@dataclass(frozen=True)
class Chunk:
    source: str  # nama file relatif terhadap folder dokumen
    index: int  # urutan chunk di dalam file
    text: str


def split_text(text: str, chunk_size: int = 120, overlap: int = 30) -> list[str]:
    """Pecah teks menjadi potongan berisi `chunk_size` kata dengan `overlap` kata tumpang tindih."""
    if chunk_size <= 0:
        raise ValueError("chunk_size harus > 0")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap harus >= 0 dan < chunk_size")

    words = text.split()
    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start : start + chunk_size]))
        if start + chunk_size >= len(words):
            break
    return chunks


def load_chunks(docs_dir: str | Path, chunk_size: int = 120, overlap: int = 30) -> list[Chunk]:
    """Baca semua file .md/.txt di `docs_dir` (rekursif) lalu pecah menjadi chunk."""
    docs_dir = Path(docs_dir)
    files = sorted(p for p in docs_dir.rglob("*") if p.suffix.lower() in SUPPORTED_SUFFIXES)
    if not files:
        raise FileNotFoundError(f"Tidak ada file .md/.txt di {docs_dir}")

    chunks: list[Chunk] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for i, piece in enumerate(split_text(text, chunk_size, overlap)):
            chunks.append(Chunk(str(path.relative_to(docs_dir)), i, piece))
    return chunks
