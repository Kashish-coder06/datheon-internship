# Task 4: Interactive Streamlit RAG & Agent Web UI

A responsive web interface built with **Streamlit** and **LangChain**, featuring:
- **Real-Time Token Streaming**: Watch the AI stream responses token-by-token using `st.write_stream`.
- **Chat Message History**: Persistent multi-turn conversations stored in `st.session_state`.
- **Mode Switching**: Switch between **RAG Document QA** (with source page citations) and **Multi-Tool Autonomous Agent** (Web search + Calculator + File reader).
- **File Uploader**: Upload your own PDF / TXT documents directly in the browser to query them instantly.
- **Session State Controls**: Reset chat history, adjust model parameters, and configure API keys seamlessly.

---

## 🛠️ Project Structure
```text
task4-streamlit-rag-agent-ui/
├── app.py                # Main Streamlit application
├── streaming_engine.py   # Token streaming & LangChain callbacks
├── requirements.txt      # Dependencies
├── .env.example          # Environment variables template
└── README.md             # Documentation & running guide
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`.
