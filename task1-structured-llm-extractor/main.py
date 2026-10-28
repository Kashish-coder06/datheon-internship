import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from schemas import InvoiceSchema, ResumeSchema
from extractor import LLMExtractor


def main():
    parser = argparse.ArgumentParser(
        description="Structured LLM Prompt Pipeline & JSON Extractor (Task 1)"
    )
    parser.add_argument(
        "--type",
        choices=["invoice", "resume"],
        required=True,
        help="Type of document to parse (invoice or resume)"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the unstructured text document"
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        default="gemini",
        help="LLM provider to use (default: gemini)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name (e.g., gemini-3.8-flash, gpt-4o-mini)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to save validated JSON output"
    )

    args = parser.parse_args()

    input_file = Path(args.file)
    if not input_file.exists():
        print(f"Error: File not found at '{args.file}'", file=sys.stderr)
        sys.exit(1)

    raw_text = input_file.read_text(encoding="utf-8")

    print(f"\n🚀 Initializing Extractor...")
    print(f"• Document Type: {args.type.upper()}")
    print(f"• Provider:      {args.provider.upper()}")
    print(f"• Source File:   {args.file}")

    schema_class = InvoiceSchema if args.type == "invoice" else ResumeSchema

    try:
        extractor = LLMExtractor(provider=args.provider, model_name=args.model)
        print(f"• Sending prompt to {args.provider} LLM with few-shot context & JSON schema...\n")
        
        result_obj = extractor.extract(
            doc_type=args.type,
            raw_text=raw_text,
            schema_class=schema_class
        )

        formatted_json = result_obj.model_dump_json(indent=2)
        print("✅ Validation Successful! Extracted Structured JSON:")
        print("=" * 60)
        print(formatted_json)
        print("=" * 60)

        if args.output:
            out_path = Path(args.output)
            out_path.write_text(formatted_json, encoding="utf-8")
            print(f"\n💾 Saved structured output to: {out_path.resolve()}")

    except Exception as e:
        print(f"\n❌ Extraction or Validation Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
