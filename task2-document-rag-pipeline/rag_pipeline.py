import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
load_dotenv()

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma

# Embedding options
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    HAS_HUGGINGFACE = True
except ImportError:
    HAS_HUGGINGFACE = False


class DocumentRAGPipeline:
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        chunk_size: int = 600,
        chunk_overlap: int = 100,
        provider: str = "gemini",
        embedding_model: Optional[str] = None,
        llm_model: Optional[str] = None
    ):
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.provider = provider.lower()
        self.embedding_model = embedding_model
        self.llm_model = llm_model

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        self.embeddings = self._init_embeddings()
        self.llm = self._init_llm()
        self.vector_store: Optional[Chroma] = None

    def _init_embeddings(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if self.provider == "gemini" and gemini_key and HAS_GOOGLE:
            model = self.embedding_model or "models/text-embedding-004"
            return GoogleGenerativeAIEmbeddings(model=model, google_api_key=gemini_key)
        elif self.provider == "openai" and openai_key and HAS_OPENAI:
            model = self.embedding_model or "text-embedding-3-small"
            return OpenAIEmbeddings(model=model, api_key=openai_key)
        elif HAS_HUGGINGFACE:
            # Local fallback embedding model requiring no API keys
            model_name = self.embedding_model or "all-MiniLM-L6-v2"
            return HuggingFaceEmbeddings(model_name=model_name)
        else:
            raise RuntimeError(
                "No embedding provider available. Set GEMINI_API_KEY or OPENAI_API_KEY, "
                "or install sentence-transformers for local embeddings."
            )

    def _init_llm(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if self.provider == "gemini" and gemini_key and HAS_GOOGLE:
            model = self.llm_model or "gemini-1.5-flash"
            return ChatGoogleGenerativeAI(model=model, google_api_key=gemini_key, temperature=0.0)
        elif self.provider == "openai" and openai_key and HAS_OPENAI:
            model = self.llm_model or "gpt-4o-mini"
            return ChatOpenAI(model=model, api_key=openai_key, temperature=0.0)
        return None

    def load_document(self, file_path: str) -> List[Document]:
        """Loads a PDF or TXT file into a list of Document objects."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found at: {file_path}")

        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            docs = loader.load()
        else:
            loader = TextLoader(str(path), encoding="utf-8")
            docs = loader.load()

        return docs

    def index_document(self, file_path: str, collection_name: str = "custom_docs") -> int:
        """Loads, recursively chunks, embeds, and stores documents in ChromaDB."""
        docs = self.load_document(file_path)
        chunks = self.text_splitter.split_documents(docs)

        # Standardize metadata citations
        for idx, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = idx + 1
            if "page" not in chunk.metadata:
                chunk.metadata["page"] = 1
            else:
                chunk.metadata["page"] = chunk.metadata["page"] + 1  # 1-indexed

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=collection_name
        )
        return len(chunks)

    def query(self, question: str, k: int = 3) -> Dict[str, Any]:
        """
        Retrieves top-k context chunks and returns grounded answer with page citations.
        """
        if self.vector_store is None:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="custom_docs"
            )

        # Retrieve relevant chunks
        retrieved_docs = self.vector_store.similarity_search_with_score(question, k=k)

        context_blocks = []
        citations = []

        for doc, score in retrieved_docs:
            source = Path(doc.metadata.get("source", "Unknown")).name
            page = doc.metadata.get("page", 1)
            chunk_id = doc.metadata.get("chunk_id", "N/A")

            context_blocks.append(
                f"[Source: {source} | Page: {page} | Chunk: {chunk_id}]\n{doc.page_content}"
            )
            citations.append({
                "source": source,
                "page": page,
                "chunk_id": chunk_id,
                "similarity_score": round(float(score), 4),
                "content_preview": doc.page_content[:180].replace("\n", " ") + "..."
            })

        context_str = "\n\n---\n\n".join(context_blocks)

        strict_system_prompt = f"""You are a strict QA document assistant. 
Answer the user's question ONLY using the facts present in the following context.
If the answer cannot be determined directly from the context, state: 'The provided document does not contain information to answer this question.'
Always mention the source document and page number for each fact stated in your answer.

CONTEXT:
{context_str}

QUESTION:
{question}
"""

        if self.llm:
            response = self.llm.invoke(strict_system_prompt)
            answer_text = response.content
        else:
            # Fallback when no LLM API key is passed (pure semantic retriever + context display)
            answer_text = (
                "[Notice: No live LLM API key detected. Showing retrieved context and citations directly]\n"
                f"Most relevant retrieved facts:\n\n{context_str}"
            )

        return {
            "question": question,
            "answer": answer_text,
            "citations": citations
        }
