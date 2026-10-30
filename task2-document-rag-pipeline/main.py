import argparse
import sys
from pathlib import Path
from rag_pipeline import DocumentRAGPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Task 2: Custom Document RAG Pipeline with Source Page Citations"
    )
    parser.add_argument(
        "--doc",
        type=str,
        default="docs/company_policy.pdf",
        help="Path to PDF or TXT document to index"
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Question to ask against the document"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start an interactive Q&A session"
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        default="gemini",
        help="LLM provider for QA answering (default: gemini)"
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=3,
        help="Number of context chunks to retrieve (default: 3)"
    )

    args = parser.parse_args()

    doc_path = Path(args.doc)
    if not doc_path.exists():
        print(f"Error: Document not found at {args.doc}", file=sys.stderr)
        print("Tip: Run 'python create_sample_pdf.py' to generate a sample PDF document.", file=sys.stderr)
        sys.exit(1)

    print("=" * 70)
    print(" TASK 2: CUSTOM DOCUMENT RAG PIPELINE (CHROMA + LANGCHAIN)")
    print("=" * 70)
    print(f"• Ingesting & Indexing document: {doc_path.resolve()}")
    
    pipeline = DocumentRAGPipeline(provider=args.provider)
    num_chunks = pipeline.index_document(str(doc_path))
    print(f"• Document successfully indexed into ChromaDB ({num_chunks} recursive chunks created).\n")

    if args.interactive:
        print("Entering interactive mode. Type 'exit' or 'quit' to stop.\n")
        while True:
            try:
                user_q = input("\nAsk Question: ").strip()
                if user_q.lower() in ["exit", "quit"]:
                    break
                if not user_q:
                    continue

                res = pipeline.query(user_q, k=args.top_k)
                print("\n" + "=" * 50)
                print(f"ANSWER:\n{res['answer']}")
                print("\nSOURCE PAGE CITATIONS:")
                for c in res["citations"]:
                    print(f" - [{c['source']}] Page {c['page']} (Chunk #{c['chunk_id']})")
                print("=" * 50)
            except KeyboardInterrupt:
                break
    elif args.query:
        res = pipeline.query(args.query, k=args.top_k)
        print("=" * 50)
        print(f"QUESTION: {args.query}\n")
        print(f"ANSWER:\n{res['answer']}\n")
        print("SOURCE CITATIONS:")
        for c in res["citations"]:
            print(f" - [{c['source']}] Page {c['page']} (Chunk #{c['chunk_id']}) | Score: {c['similarity_score']}")
            print(f"   Excerpt: {c['content_preview']}\n")
        print("=" * 50)
    else:
        print("Please provide a question via --query 'your question' or use --interactive mode.")


if __name__ == "__main__":
    main()
