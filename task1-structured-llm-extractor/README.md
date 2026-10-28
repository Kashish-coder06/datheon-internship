# Task 1: Structured LLM Prompt Pipeline & JSON Extractor

A production-ready pipeline for extracting structured data from unstructured text using LLMs (Google Gemini / OpenAI), parameterized prompt templates with few-shot learning, and strict Pydantic validation.

---

## 📌 Features
- **Multi-Provider Support**: Supports **Google Gemini** (`google-genai`) and **OpenAI** (`openai`).
- **Validated Pydantic Schemas**:
  - `InvoiceSchema`: Line items, vendor, customer, totals, currency, dates, tax calculations.
  - `ResumeSchema`: Candidate profile, education, skills, work experiences, certifications, contact details.
- **Parameterized Prompt Templates**: Few-shot contextual examples with strict instruction bounds.
- **Automatic Fallback & JSON Cleaning**: Handles markdown backticks, malformed formats, and validates fields against Pydantic models.
- **Interactive CLI & Batch Mode**: Includes sample unstructured documents for testing out-of-the-box.

---

## 🛠️ Project Structure
```text
task1-structured-llm-extractor/
├── main.py               # Main CLI execution script
├── schemas.py            # Pydantic data schemas (Invoice & Resume)
├── prompt_templates.py   # Parameterized few-shot prompt builders
├── extractor.py          # LLM pipeline engine (Gemini & OpenAI)
├── samples/
│   ├── sample_invoice.txt
│   └── sample_resume.txt
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

### 2. Configure API Keys
Copy `.env.example` to `.env` and insert your API key:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
# Optional:
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Extractor

#### Test with Sample Invoice:
```bash
python main.py --type invoice --file samples/sample_invoice.txt
```

#### Test with Sample Resume:
```bash
python main.py --type resume --file samples/sample_resume.txt
```

#### Save Output to JSON:
```bash
python main.py --type invoice --file samples/sample_invoice.txt --output result_invoice.json
```
