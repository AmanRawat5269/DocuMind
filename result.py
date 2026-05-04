import streamlit as st
from dotenv import load_dotenv
import tempfile
import os

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()
st.set_page_config(page_title="Agentic RAG System", layout="wide")

SYSTEM_PROMPT = """You are an intelligent AI assistant with strong reasoning ability.

TOOL USAGE RULES:
- If the user has uploaded documents and the question seems related to them → use search_uploads
- If the question requires searching a knowledge base or database → use search_papers
- If the question requires current, latest, or real-time information → use web_search
- If you can answer confidently and correctly from your own knowledge → answer directly

DECISION LOGIC:
- Think about what kind of information is needed
- Choose the most appropriate tool based on the nature of the question
- If a tool returns weak or irrelevant results → try another tool or answer directly
- Never force a tool call if it is not needed

ANSWER QUALITY:
- Give well-explained, clear answers
- Minimum 7-8 sentences for most questions
- Use bullet points or numbered lists when comparing or listing multiple things
- Explain with examples where helpful

IMPORTANT:
- Never hallucinate or guess facts
- If unsure → use a tool instead of guessing
- Only return the final answer — never show tool calls or internal reasoning
"""

@st.cache_resource
def get_embedding_model():
    return OllamaEmbeddings(model="nomic-embed-text")

embedding_model = get_embedding_model()

def process_uploaded_file(uploaded_file):
    suffix = ".pdf" if uploaded_file.type == "application/pdf" else ".txt"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if suffix == ".pdf":
        docs = PyPDFLoader(tmp_path).load()
    else:
        with open(tmp_path, "r", encoding="utf-8") as f:
            docs = [Document(page_content=f.read(), metadata={"source": uploaded_file.name})]

    os.unlink(tmp_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    vs = Chroma(
        embedding_function=embedding_model,
        persist_directory="my_chroma_db",
        collection_name="user_uploads"
    )
    vs.add_documents(chunks)

    return len(chunks)

def clear_user_uploads():
    import chromadb
    client = chromadb.PersistentClient(path="my_chroma_db")
    try:
        client.delete_collection("user_uploads")
        return True
    except:
        return False

def has_user_uploads():
    import chromadb
    client = chromadb.PersistentClient(path="my_chroma_db")
    try:
        return client.get_collection("user_uploads").count() > 0
    except:
        return False

def format_context(docs):
    return "\n\n".join([
        f"(Source: {doc.metadata.get('source','unknown')})\n{doc.page_content}"
        for doc in docs
    ])

def get_response_style(user_input):
    u = user_input.lower()
    if "one word" in u or "one line" in u:
        return "Respond in exactly one line."
    elif "short" in u or "brief" in u:
        return "Give a short and concise answer."
    elif "detail" in u or "in depth" in u:
        return "Give a very detailed answer with examples."
    return "Give a well-explained answer in 4-6 sentences. Use bullet points if listing or comparing."

@st.cache_resource
def load_agent():
    llm = ChatOllama(model="llama3.1", temperature=0)
    tavily = TavilySearch(max_results=3)

    def rerank(query, docs):
        if not docs:
            return []

        docs_text = "\n\n".join([
            f"[{i}] {doc.page_content[:300]}"
            for i, doc in enumerate(docs)
        ])

        prompt = f"""Query: {query}

Documents: 
{docs_text}

Pick top 3 most relevant docs.
Return only numbers like: 0,2,3"""

        try:
            res = llm.invoke(prompt).content
            idx = [int(i.strip()) for i in res.split(",") if i.strip().isdigit()]
            ranked = [docs[i] for i in idx if i < len(docs)]
            return ranked if ranked else docs[:3]
        except:
            return docs[:3]

    def is_relevant(query, docs):
        if not docs:
            return False

        content = "\n\n".join([d.page_content[:200] for d in docs])

        prompt = f"""Query: {query}

Context:
{content}

Is this useful?

Answer ONLY YES or NO"""

        try:
            res = llm.invoke(prompt).content.upper()
            return "YES" in res
        except:
            return False

    def retrieve(collection, query):
        vs = Chroma(
            embedding_function=embedding_model,
            persist_directory="my_chroma_db",
            collection_name=collection
        )

        results = vs.similarity_search_with_score(query, k=12)

        if not results:
            return []

        filtered = [doc for doc, score in results if score <= 0.6]
        docs = filtered if filtered else [doc for doc, _ in results[:3]]

        return rerank(query, docs)

    @tool
    def search_uploads(query: str) -> str:
        """Search user uploaded documents."""
        docs = retrieve("user_uploads", query)
        if not is_relevant(query, docs):
            return "NOT_RELEVANT"
        return format_context(docs[:3])

    @tool
    def search_papers(query: str) -> str:
        """Search research paper database."""
        docs = retrieve("research_paper", query)
        if not is_relevant(query, docs):
            return "NOT_RELEVANT"
        return format_context(docs[:3])

    @tool
    def web_search(query: str) -> str:
        """Search web for latest or current information."""
        return str(tavily.invoke(query))

    return create_react_agent(
        model=llm,
        tools=[search_uploads, search_papers, web_search],
        prompt=SYSTEM_PROMPT
    )

agent = load_agent()

def get_recent_context():
    history = st.session_state.messages[-6:]
    return [{"role": m["role"], "content": m["content"]} for m in history]

def detect_source(msgs):
    sources = set()
    for m in msgs:
        name = getattr(m, "name", None)
        if name == "search_papers":
            sources.add("database")
        elif name == "search_uploads":
            sources.add("uploads")
        elif name == "web_search":
            sources.add("web")
    return ", ".join(sources) if sources else "model knowledge"

def show_source_badges(source):
    if "database" in source:
        st.caption("Source: Database")
    if "uploads" in source:
        st.caption("Source: Upload")
    if "web" in source:
        st.caption("Source: Web")
    if source == "model knowledge":
        st.caption("Model Knowledge")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

with st.sidebar:
    st.title("Upload")

    file = st.file_uploader("PDF or TXT", type=["pdf", "txt"])

    if file and file.name not in st.session_state.uploaded_files:
        n = process_uploaded_file(file)
        st.session_state.uploaded_files.append(file.name)
        st.success(f"{file.name} → {n} chunks")

    if st.button("Clear Uploads"):
        clear_user_uploads()
        st.session_state.uploaded_files = []
        st.rerun()

st.title("Agentic RAG System")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "source" in m:
            show_source_badges(m["source"])

inp = st.chat_input("Ask anything...")

if inp:
    st.session_state.messages.append({"role": "user", "content": inp})

    with st.chat_message("user"):
        st.markdown(inp)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                msgs = get_recent_context()

                if has_user_uploads():
                    msgs.append({
                        "role": "system",
                        "content": "User has uploaded docs. Use them if relevant."
                    })

                style = get_response_style(inp)
                if style:
                    msgs.append({"role": "system", "content": style})

                msgs.append({"role": "user", "content": inp})

                res = agent.invoke({"messages": msgs})

                final_msg = None
                for m in reversed(res["messages"]):
                    if hasattr(m, "content") and m.content and not getattr(m, "tool_calls", None):
                        final_msg = m.content
                        break

                out = final_msg if final_msg else "No response generated."
                src = detect_source(res["messages"])

            except Exception as e:
                out = str(e)
                src = "model knowledge"

        st.markdown(out)
        show_source_badges(src)

        st.session_state.messages.append({
            "role": "assistant",
            "content": out,
            "source": src
        })