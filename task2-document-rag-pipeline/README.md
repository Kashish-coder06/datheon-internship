# Task 2: Custom Document RAG Pipeline with Citations

A complete Retrieval-Augmented Generation (RAG) pipeline built with **LangChain**, **ChromaDB**, and modern LLMs (Google Gemini / OpenAI / Local HuggingFace embeddings).

---

## 📌 Features
- **Document Ingestion**: Supports PDF (`PyPDFLoader`) and Plain Text (`TextLoader`) files.
- **Recursive Chunking**: Smart chunking using `RecursiveCharacterTextSplitter` with configurable chunk size and overlap.
- **Vector Storage**: Persistent vector database using **ChromaDB**.
- **Strict Grounded QA**: Answers queries strictly from the retrieved document context to prevent hallucinations.
- **Source Page Citations**: Every answer includes exact source document names and page numbers/chunks cited.
- **Interactive CLI & Standalone Demo**: Run interactive Q&A or automated test queries.

---

## 🛠️ Project Structure
```text
task2-document-rag-pipeline/
├── rag_pipeline.py       # Core RAG indexing and QA engine
├── main.py               # Interactive CLI for querying documents
├── demo_rag.py           # Self-contained demo script with source citations
├── create_sample_pdf.py  # Utility script to generate a multi-page test PDF
├── docs/                 # Directory to drop your PDF/TXT files
│   └── company_policy.pdf
├── chroma_db/            # Local persistent Chroma vector store
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional for API LLMs)
Copy `.env.example` to `.env`:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Generate Sample Multi-Page PDF
```bash
python create_sample_pdf.py
```

### 4. Run the Extractor / Q&A CLI

#### Ingest and Ask a Question:
```bash
python main.py --doc docs/company_policy.pdf --query "What is the remote work equipment allowance?"
```

#### Interactive Q&A Mode:
```bash
python main.py --doc docs/company_policy.pdf --interactive
```

#### Run Instant Offline Demo:
```bash
python demo_rag.py
```
