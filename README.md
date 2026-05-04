# DocuMind - Agentic RAG Document Assistant

DocuMind is an AI-powered document assistant that enables organizations and individuals to upload their documents and interact with them using natural language.

It uses Retrieval-Augmented Generation (RAG) combined with an intelligent agent to provide accurate, context-aware answers from multiple sources.

---

## 🚀 Use Case

DocuMind is designed for real-world scenarios such as:

* Companies querying internal documents
* Students interacting with study materials
* Teams searching knowledge bases
* Anyone who wants to "chat with their documents"

---

## ✨ Features

* 📄 Upload and query PDF or TXT documents
* 🧠 Intelligent agent for dynamic decision-making
* 🔍 Semantic search using vector embeddings
* 🧩 Chunking + reranking for improved accuracy
* 🌐 Optional web search for real-time information
* 📌 Source tracking (Upload / Web / Model Knowledge)
* 💬 Context-aware conversational memory

---

## 🛠️ Tech Stack

* Streamlit (UI)
* LangChain (RAG pipeline)
* LangGraph (Agent orchestration)
* ChromaDB (Vector database)
* Ollama (LLaMA 3.1 - Local LLM)
* Tavily Search (Web search tool)

---

## ⚙️ How It Works

1. Documents are uploaded and split into chunks
2. Chunks are converted into embeddings and stored in ChromaDB
3. On query:

   * Relevant chunks are retrieved
   * Low-quality matches are filtered
   * Top chunks are reranked using LLM
4. Agent decides:

   * Use uploaded docs
   * Use web search
   * Or answer directly
5. Final response is generated with source awareness

---

## 🧪 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run result.py
```

Make sure:

* Ollama is running locally
* Required models are installed

---

## 📸 Demo / Screenshots

<img width="1919" height="880" alt="image" src="https://github.com/user-attachments/assets/9075b1db-b3fc-422f-8677-a3c1c069b715" />

---
<img width="1902" height="888" alt="image" src="https://github.com/user-attachments/assets/f0b2d781-e53b-4851-aa01-222b85aa43ba" />



---

## 👨‍💻 Author

Aman Rawat
