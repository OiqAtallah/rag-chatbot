"""Antarmuka command line."""

import argparse
import sys

from .chatbot import RagChatbot


def main(argv: list[str] | None = None) -> int:
    try:
        from dotenv import load_dotenv

        load_dotenv()  # baca ANTHROPIC_API_KEY dari file .env bila ada
    except ImportError:
        pass

    parser = argparse.ArgumentParser(prog="rag_chatbot", description="Chatbot RAG sederhana")
    parser.add_argument("--docs", default="data/docs", help="folder dokumen .md/.txt")
    parser.add_argument("--k", type=int, default=3, help="jumlah chunk yang diambil")
    parser.add_argument("--dry-run", action="store_true", help="hanya tampilkan hasil retrieval, tanpa memanggil API")
    parser.add_argument("question", nargs="?", help="pertanyaan; kosongkan untuk mode interaktif")
    args = parser.parse_args(argv)

    try:
        bot = RagChatbot(args.docs, k=args.k)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    def handle(question: str) -> None:
        if args.dry_run:
            hits = bot.retrieve(question)
            print("Chunk terambil:" if hits else "Tidak ada chunk relevan.")
            for h in hits:
                print(f"\n[{h.chunk.source}#{h.chunk.index}] skor={h.score:.2f}\n{h.chunk.text}")
            return
        result = bot.answer(question)
        print(result.text)
        if result.hits:
            print("\nSumber:")
            for h in result.hits:
                print(f"  - [{h.chunk.source}#{h.chunk.index}] skor={h.score:.2f}")

    if args.question:
        handle(args.question)
        return 0

    print("Mode interaktif. Ketik 'keluar' untuk berhenti.")
    while True:
        try:
            question = input("\nTanya> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in {"keluar", "exit", "quit"}:
            break
        if question:
            handle(question)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
