# RAG Chatbot Sederhana (Python + Claude API)

![tests](https://github.com/USERNAME/rag-chatbot/actions/workflows/ci.yml/badge.svg)

Chatbot tanya-jawab dokumen berbasis **Retrieval-Augmented Generation (RAG)**. Pertanyaan dijawab oleh LLM
**hanya** berdasarkan potongan dokumen yang relevan, lengkap dengan sumber kutipannya.

> Ganti `USERNAME` pada badge di atas dengan username GitHub kamu setelah repo dibuat.

## Cara kerja

```
 dokumen (.md/.txt)
        │  split per ~120 kata (overlap 30)
        ▼
     chunks ──► TF-IDF index
                    │
 pertanyaan ──► cari top-k chunk (cosine similarity)
                    │
                    ▼
      prompt = konteks + pertanyaan ──► Claude API ──► jawaban + sumber [file#chunk]
```

Jika tidak ada chunk yang cukup relevan, chatbot menjawab bahwa informasi tidak ditemukan **tanpa memanggil API**
(hemat biaya dan mengurangi risiko halusinasi).

## Struktur proyek

```
rag_chatbot/
  loader.py      # baca dokumen & chunking
  retriever.py   # TF-IDF + cosine similarity
  llm.py         # prompt & pemanggilan Claude API
  chatbot.py     # alur RAG (retrieve -> generate)
  cli.py         # antarmuka command line
data/docs/       # contoh dokumen (metrik bisnis, SQL, kualitas data)
tests/           # pytest (tanpa API key; LLM diganti fake)
.github/workflows/ci.yml   # CI: jalankan pytest di setiap push/PR
```

## Instalasi

Butuh Python 3.11+.

```bash
git clone https://github.com/USERNAME/rag-chatbot.git
cd rag-chatbot
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # lalu isi ANTHROPIC_API_KEY
```

API key dibuat di [console.anthropic.com](https://console.anthropic.com). File `.env` sudah masuk `.gitignore`.

## Penggunaan

```bash
# satu pertanyaan
python -m rag_chatbot "Apa bedanya WHERE dan HAVING?"

# mode interaktif
python -m rag_chatbot

# lihat hasil retrieval saja, tanpa API key
python -m rag_chatbot --dry-run "Apa itu churn rate?"
```

Contoh keluaran `--dry-run` (nyata, dipotong):

```
Chunk terambil:

[metrik_bisnis.md#0] skor=0.24
# Metrik Bisnis Umum Churn rate adalah persentase pelanggan yang berhenti menggunakan produk ...
```

Pertanyaan di luar dokumen (`--dry-run "resep nasi goreng"`) menghasilkan `Tidak ada chunk relevan.`

Opsi: `--docs <folder>` untuk memakai dokumen sendiri (file `.md`/`.txt`), `--k <n>` jumlah chunk konteks.
Model dapat diganti lewat variabel `ANTHROPIC_MODEL`.

## Testing

```bash
pytest -q
```

Test mencakup chunking, kualitas retrieval (pertanyaan -> dokumen yang benar), dan alur RAG dengan LLM palsu,
sehingga berjalan tanpa API key dan gratis.

## Keputusan desain & keterbatasan

- **TF-IDF, bukan embedding.** Dipilih agar sederhana, cepat, dan tanpa dependensi/biaya tambahan. Kelemahannya:
  tidak menangkap sinonim (mis. "pelanggan berhenti" vs "churn"). Retriever dipisah di `retriever.py`
  sehingga mudah diganti.
- **Chunking berbasis kata**, belum mempertimbangkan struktur heading/paragraf.
- **Belum ada memori percakapan**; tiap pertanyaan berdiri sendiri.
- **Belum ada evaluasi otomatis kualitas jawaban**; test hanya memeriksa retrieval dan alur.

## Pengembangan lanjutan

- [ ] Retriever embedding (mis. sentence-transformers) + vector store (FAISS/Chroma), bandingkan dengan TF-IDF
- [ ] Dataset evaluasi kecil (pertanyaan + dokumen sumber benar) untuk mengukur hit rate@k
- [ ] Riwayat percakapan dan penulisan ulang pertanyaan lanjutan
- [ ] Antarmuka web (Streamlit/Gradio)

## Lisensi

MIT
