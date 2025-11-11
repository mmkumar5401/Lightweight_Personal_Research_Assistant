
# 🧠 Lightweight Personal Research Assistant

A **Retrieval-Augmented Generation (RAG)**-based local research assistant that helps you **query, summarize, and analyze academic papers**.  
It uses **LangChain**, **ChromaDB**, and **Ollama (LLaMA3 / Mistral)** to give you fast, context-aware answers — entirely offline.

---

## 🚀 Features

- 🔍 Searches across your local research papers (PDFs)
- 🧠 Answers contextually using RAG (Retrieval-Augmented Generation)
- 🧩 Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- ⚙️ Powered by **FastAPI** backend and **Ollama** for local LLM inference
- 💬 Offers both **REST API** and **CLI** interfaces
- 💾 Fully local — no API calls, no data leaks

---

## 🧰 Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.12+** | Runtime |
| **LangChain** | Orchestrates RAG pipeline |
| **ChromaDB** | Vector store for text embeddings |
| **Ollama** | Runs local LLMs (LLaMA3 / Mistral) |
| **Sentence-Transformers** | Text embedding model |
| **FastAPI + Uvicorn** | Backend API |
| **Rich** | CLI formatting |

---

## 📦 Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mmkumar5401/Lightweight_Personal_Research_Assistant.git
cd Lightweight_Personal_Research_Assistant
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Ollama (for macOS)

```bash
brew install ollama/tap/ollama
ollama serve
```

Then pull your model of choice:

```bash
ollama pull llama3
# or
ollama pull mistral
```

---

## 🧩 Project Structure

```
Lightweight_Personal_Research_Assistant/
│
├── backend/
│   ├── main.py              # FastAPI backend
│   ├── rag_engine.py        # Core RAG logic (loading, embeddings, retrieval)
│   ├── data/
│   │   ├── papers/          # Folder containing all your PDFs
│   │   └── vector_store/    # Folder for ChromaDB persistence
│
├── cli.py                   # Interactive CLI interface
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Run the Assistant

### ▶️ Run the FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

You’ll see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
System initialized.
```

Once started, it automatically loads your PDFs, chunks them, embeds them, and builds a vector store for retrieval.

You can then send queries to the API:

```bash
curl -X POST http://127.0.0.1:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the research gaps in knowledge tracing?"}'
```

Expected output:

```json
{
  "answer": "Potential research gaps include interpretability, fairness, and inclusion of behavioral context in knowledge tracing models..."
}
```

---

### 💬 Run via CLI

If you prefer a lightweight interface:

```bash
python cli.py
```

Example session:

```
🎓 Thesis Research Copilot (CLI Mode)
Type 'exit' to quit.

❓ Ask: What do these papers talk about?

🧠 Answer:
The papers primarily discuss methods in Knowledge Tracing (KT), focusing on modeling student learning patterns...
```

---

## 🧠 How It Works

1. **PDF ingestion:** PDFs are read from `backend/data/papers/`
2. **Text chunking:** Each document is split into overlapping chunks
3. **Embedding:** Each chunk is encoded with a transformer model
4. **Storage:** Embeddings are persisted in ChromaDB
5. **Retrieval:** The top `k` most relevant chunks are fetched per query
6. **Answer generation:** Ollama’s local model (LLaMA3/Mistral) forms a final response using the retrieved context

---

## ⚙️ Configuration

You can tweak parameters inside `backend/rag_engine.py`:

| Parameter         | Description                    | Default                                  |
| ----------------- | ------------------------------ | ---------------------------------------- |
| `chunk_size`      | Tokens per chunk               | 1000                                     |
| `chunk_overlap`   | Overlap between chunks         | 200                                      |
| `embedding_model` | Embedding model                | `sentence-transformers/all-MiniLM-L6-v2` |
| `llm_model`       | LLM used via Ollama            | `llama3`                                 |
| `retriever_k`     | Number of top chunks retrieved | 8                                        |

---

## 🧪 Example Queries

* “Summarize the categories of knowledge tracing models.”
* “List future research directions discussed in these papers.”
* “Compare behavior-aware and graph-based KT approaches.”
* “What datasets are most used in KT research?”

---

## 🧩 Troubleshooting

| Issue                            | Explanation / Fix                                            |
| -------------------------------- | ------------------------------------------------------------ |
| `I don’t know` response          | The question didn’t match your PDFs; increase `retriever_k`  |
| `TypeError: TextEncodeInput`     | Some PDFs have hidden characters — handled automatically now |
| `Failed to send telemetry event` | Harmless Chroma warning — ignore                             |
| `Ollama not found`               | Make sure `ollama serve` is running                          |

---

## 💡 Future Enhancements

* Add PDF upload and auto-refresh of embeddings
* Integrate citation extraction and BibTeX export
* Build a simple web UI dashboard
* Support multi-modal research documents

---

## 📄 License

MIT License © 2025 [Manojkumar Muthukumaran](https://github.com/mmkumar5401)

```

```
