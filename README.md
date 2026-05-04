# DocuMind – Privacy-First Agentic RAG System

DocuMind is a privacy-focused AI document assistant designed for organizations that need to interact with their internal data **without exposing it to external LLM APIs**.

Unlike typical AI tools, DocuMind runs locally using Ollama and combines Retrieval-Augmented Generation (RAG) with an intelligent agent to deliver **accurate, context-aware, and source-grounded answers** from multiple data sources.

It is built to handle real-world enterprise scenarios where **data security, reliability, and explainability** are critical.

---

## 🚀 Use Cases

DocuMind is designed for practical, real-world applications such as:

- 🏢 Companies querying internal and confidential documents
- 📚 Students interacting with personal study materials
- 🧠 Teams exploring internal knowledge bases
- 🔐 Organizations that cannot send sensitive data to tools like ChatGPT or Claude

---
## 🔐 Why Not Just Use ChatGPT or Claude?

Most AI tools require sending data to external servers, which creates serious privacy and compliance concerns.

DocuMind solves this by:

- Running fully locally using Ollama
- Keeping all documents and queries on-device
- Avoiding external API calls for sensitive data
- Providing controlled, document-grounded answers instead of hallucinated responses

This makes it ideal for enterprise environments where **data privacy is non-negotiable**.

---

## 🏆 Key Differentiators

- 🔒 Privacy-first architecture (local LLM with Ollama)
- 🤖 Agent-based tool selection (documents, database, web)
- 📄 Retrieval-Augmented Generation (RAG) pipeline
- 🎯 Relevance filtering and reranking for better answers
- 🌐 Multi-source intelligence (Uploads + DB + Web)
- ⚙️ Modular and extensible system design
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

### 💬 Chat Interface
Clean Streamlit-based chat UI with document upload support and source tracking.
<img width="1919" height="903" alt="Screenshot 2026-05-04 231938" src="https://github.com/user-attachments/assets/b85efc0f-aef3-4919-804a-dadc1b1ba880" />

---

### 📄 Answer from Uploaded Document
Example where the system retrieves context from user-uploaded files and generates grounded answers.
<img width="1919" height="890" alt="image" src="https://github.com/user-attachments/assets/417bc397-8d3c-4da4-b4ba-7e3ee437c2d6" />

---
### 🌐 Answer using Web Search
When local context is insufficient, the agent intelligently falls back to real-time web search.

<img width="1902" height="888" alt="image" src="https://github.com/user-attachments/assets/f0b2d781-e53b-4851-aa01-222b85aa43ba" />



---

## 👨‍💻 Author

Aman Rawat
