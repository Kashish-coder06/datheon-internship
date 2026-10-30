import os
import time
import sys
from pathlib import Path
from typing import Generator, Dict, Any, List

# Add parent path so we can import Task 2 and Task 3 modules directly
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir / "task2-document-rag-pipeline"))
sys.path.append(str(base_dir / "task3-multi-tool-agent"))

try:
    from rag_pipeline import DocumentRAGPipeline
except ImportError:
    DocumentRAGPipeline = None

try:
    from agent import ResearchAgentExecutor
except ImportError:
    ResearchAgentExecutor = None


def stream_text_generator(full_text: str, delay: float = 0.02) -> Generator[str, None, None]:
    """Simulates real-time streaming tokens for smooth UI output."""
    words = full_text.split(" ")
    for idx, word in enumerate(words):
        yield word + (" " if idx < len(words) - 1 else "")
        time.sleep(delay)


class AppBackendEngine:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.rag_pipeline = None
        self.agent_executor = None

    def get_rag_pipeline(self):
        if self.rag_pipeline is None and DocumentRAGPipeline:
            self.rag_pipeline = DocumentRAGPipeline(provider=self.provider)
        return self.rag_pipeline

    def get_agent_executor(self):
        if self.agent_executor is None and ResearchAgentExecutor:
            self.agent_executor = ResearchAgentExecutor(provider=self.provider)
        return self.agent_executor
