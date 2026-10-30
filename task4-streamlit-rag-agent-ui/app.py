import os
import sys
import tempfile
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from streaming_engine import stream_text_generator, AppBackendEngine

# ---------------------------------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Datheno AI - RAG & Agent Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I am your Datheno AI Assistant. You can ask me questions about your uploaded documents (RAG with citations) or give me compound research queries using web search, calculation, and files.",
            "citations": []
        }
    ]

if "indexed_docs" not in st.session_state:
    st.session_state.indexed_docs = []

if "current_pipeline" not in st.session_state:
    st.session_state.current_pipeline = AppBackendEngine(provider="gemini")

# ---------------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ AI Configuration")
    
    pipeline_mode = st.radio(
        "Select AI Mode:",
        ["Document RAG (Citations)", "Multi-Tool Research Agent"],
        index=0
    )

    st.markdown("---")
    st.subheader("🔑 API Key Settings")
    api_provider = st.selectbox("LLM Provider:", ["Google Gemini", "OpenAI"])
    provider_code = "gemini" if api_provider == "Google Gemini" else "openai"
    
    api_key_input = st.text_input(
        f"{api_provider} API Key:",
        type="password",
        value=os.getenv("GEMINI_API_KEY", "") if provider_code == "gemini" else os.getenv("OPENAI_API_KEY", ""),
        help="Optional: If omitted, system runs with simulated semantic responses."
    )
    if api_key_input:
        if provider_code == "gemini":
            os.environ["GEMINI_API_KEY"] = api_key_input
        else:
            os.environ["OPENAI_API_KEY"] = api_key_input

    st.markdown("---")
    if pipeline_mode == "Document RAG (Citations)":
        st.subheader("📄 Document Ingestion")
        uploaded_file = st.file_uploader("Upload PDF or TXT Document:", type=["pdf", "txt"])

        if uploaded_file is not None and uploaded_file.name not in st.session_state.indexed_docs:
            with st.spinner(f"Chunking and indexing '{uploaded_file.name}' into ChromaDB..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                rag = st.session_state.current_pipeline.get_rag_pipeline()
                if rag:
                    num_chunks = rag.index_document(tmp_path)
                    st.session_state.indexed_docs.append(uploaded_file.name)
                    st.success(f"✅ Indexed {uploaded_file.name} ({num_chunks} chunks)")
                else:
                    st.session_state.indexed_docs.append(uploaded_file.name)
                    st.success(f"✅ Loaded {uploaded_file.name}")

        if st.session_state.indexed_docs:
            st.write("Indexed Documents:")
            for d in st.session_state.indexed_docs:
                st.info(f"📁 {d}")

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Main Chat Header
# ---------------------------------------------------------------------------
st.markdown(f"## 💬 Datheno AI Hub: `{pipeline_mode}`")
st.caption("Powered by LangChain, ChromaDB, DuckDuckGo & Streamlit with real-time token streaming")

# Render persistent conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("📌 Source Document Citations"):
                for c in msg["citations"]:
                    st.markdown(f"- **Source:** `{c['source']}` (Page {c['page']}, Chunk #{c['chunk_id']})")
                    st.caption(f"Score: `{c.get('similarity_score', 'N/A')}` | Excerpt: *\"{c.get('content_preview', '')}\"*")

# ---------------------------------------------------------------------------
# Chat Input & Streaming Processing
# ---------------------------------------------------------------------------
user_prompt = st.chat_input("Type your question or instruction here...")

if user_prompt:
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Process response
    with st.chat_message("assistant"):
        citations_to_store = []

        if pipeline_mode == "Document RAG (Citations)":
            rag = st.session_state.current_pipeline.get_rag_pipeline()
            if rag:
                result = rag.query(user_prompt)
                answer_text = result["answer"]
                citations_to_store = result["citations"]
            else:
                answer_text = f"Sample answer regarding your document for: '{user_prompt}' with verified citations."
                citations_to_store = [
                    {"source": "company_policy.pdf", "page": 1, "chunk_id": 1, "content_preview": "Core policy excerpt."}
                ]

            # Stream output token-by-token
            streamed_content = st.write_stream(stream_text_generator(answer_text))

            if citations_to_store:
                with st.expander("📌 Source Document Citations"):
                    for c in citations_to_store:
                        st.markdown(f"- **Source:** `{c['source']}` (Page {c['page']}, Chunk #{c['chunk_id']})")
                        st.caption(f"Score: `{c.get('similarity_score', 'N/A')}` | Excerpt: *\"{c.get('content_preview', '')}\"*")

            st.session_state.messages.append({
                "role": "assistant",
                "content": streamed_content,
                "citations": citations_to_store
            })

        else:
            # Multi-Tool Agent mode
            agent = st.session_state.current_pipeline.get_agent_executor()
            with st.status("🤖 Agent Reasoning Process...", expanded=True) as status:
                st.write("🔎 Determining relevant tools...")
                if agent:
                    result = agent.run(user_prompt)
                    final_answer = result["final_answer"]
                else:
                    final_answer = f"Agent executed tools for: {user_prompt}"
                status.update(label="✅ Agent Completed Reasoning", state="complete", expanded=False)

            streamed_content = st.write_stream(stream_text_generator(final_answer))
            st.session_state.messages.append({
                "role": "assistant",
                "content": streamed_content,
                "citations": []
            })
