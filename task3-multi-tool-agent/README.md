# Task 3: Autonomous Multi-Tool Research Agent

An autonomous function-calling / ReAct AI agent built with **LangChain**, capable of executing compound queries using real-time web search, an exact mathematical calculator, and local filesystem tools with a transparent reasoning chain (**Thought ➔ Action ➔ Observation ➔ Final Answer**).

---

## 📌 Features
- **Real-Time Web Search**: Queries DuckDuckGo for live world facts, current events, and statistics.
- **Python Math Calculator**: Evaluates mathematical expressions using safe python arithmetic.
- **Local File System Tool**: Reads local files, workspace documents, and data reports safely.
- **Transparent Reasoning Loop**: Full ReAct execution trace showing step-by-step cognitive steps (`Thought`, `Action`, `Action Input`, `Observation`, `Final Answer`).
- **Interactive CLI & Automated Test Suite**: Test compound multi-hop queries out-of-the-box.

---

## 🛠️ Project Structure
```text
task3-multi-tool-agent/
├── tools.py              # Tool definitions (DuckDuckGo, Calculator, File Reader)
├── agent.py              # ReAct Agent loop & LangChain function-calling engine
├── main.py               # Interactive CLI for user queries
├── demo_agent.py         # Self-contained ReAct loop demo
├── sample_data/          # Sample local files for the agent to inspect
│   └── company_metrics.txt
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
Copy `.env.example` to `.env`:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Agent

#### Compound Query (Search + Math + File):
```bash
python main.py --query "Read sample_data/company_metrics.txt, find the Q3 revenue, calculate a 15% bonus on it, and search DuckDuckGo for the current inflation rate."
```

#### Interactive Terminal Session:
```bash
python main.py --interactive
```

#### Instant Demonstration Mode (No API keys needed):
```bash
python demo_agent.py
```
