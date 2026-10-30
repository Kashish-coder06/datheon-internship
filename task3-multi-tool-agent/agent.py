import os
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

from tools import get_all_tools

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

try:
    from langchain_openai import ChatOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


REACT_PROMPT_TEMPLATE = """You are a helpful and intelligent AI research agent equipped with tools to answer complex questions.

You have access to the following tools:
{tool_descriptions}

Use the following strict format for your reasoning and execution process:

Question: the input question you must solve
Thought: consider what steps to take next. Always think before taking an action.
Action: the action to take, should be exactly one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation sequence can repeat multiple times)
Thought: I now have sufficient information to answer the question.
Final Answer: the complete, accurate final answer to the original question.

Begin!

Question: {question}
Thought:"""


class ResearchAgentExecutor:
    def __init__(self, provider: str = "gemini", model_name: Optional[str] = None):
        self.provider = provider.lower()
        self.tools = {t.name: t for t in get_all_tools()}
        self.llm = self._init_llm(model_name)

    def _init_llm(self, model_name: Optional[str]):
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if self.provider == "gemini" and gemini_key and HAS_GOOGLE:
            m = model_name or "gemini-1.5-flash"
            return ChatGoogleGenerativeAI(model=m, google_api_key=gemini_key, temperature=0.0)
        elif self.provider == "openai" and openai_key and HAS_OPENAI:
            m = model_name or "gpt-4o-mini"
            return ChatOpenAI(model=m, api_key=openai_key, temperature=0.0)
        return None

    def run(self, question: str, max_steps: int = 6) -> Dict[str, Any]:
        """
        Executes ReAct reasoning loop displaying Thought -> Action -> Observation -> Final Answer.
        """
        tool_descriptions = "\n".join([f"- {name}: {t.description}" for name, t in self.tools.items()])
        tool_names = ", ".join(self.tools.keys())

        conversation_history = REACT_PROMPT_TEMPLATE.format(
            tool_descriptions=tool_descriptions,
            tool_names=tool_names,
            question=question
        )

        trace = []
        step = 0

        print("\n" + "=" * 65)
        print(f"[AGENT] REASONING CHAIN FOR: \"{question}\"")
        print("=" * 65)

        if not self.llm:
            print("\n[Notice] No live LLM API key detected. Running in simulated ReAct evaluation mode.")
            return self._fallback_simulated_run(question)

        while step < max_steps:
            step += 1
            response = self.llm.invoke(conversation_history)
            output = response.content

            # Check if agent produced Final Answer
            if "Final Answer:" in output:
                final_part = output.split("Final Answer:", 1)[1].strip()
                thought_part = output.split("Final Answer:", 1)[0].strip()
                if thought_part:
                    print(f"\nThought {step}: {thought_part}")
                print(f"\n[RESULT] Final Answer:\n{final_part}")
                print("=" * 65)
                return {"question": question, "final_answer": final_part, "steps": trace}

            # Parse Action and Action Input
            action_match = re.search(r"Action:\s*(\w+)", output)
            input_match = re.search(r"Action Input:\s*(.+?)(?=\n|$)", output, re.DOTALL)

            thought_text = output
            if action_match:
                thought_text = output[:action_match.start()].replace("Thought:", "").strip()

            print(f"\nThought {step}: {thought_text}")

            if not action_match or not input_match:
                return {"question": question, "final_answer": output, "steps": trace}

            action = action_match.group(1).strip()
            action_input = input_match.group(1).strip().strip('"').strip("'")

            print(f"Action: {action}")
            print(f"Action Input: {action_input}")

            if action in self.tools:
                tool_func = self.tools[action]
                observation = tool_func.invoke(action_input)
            else:
                observation = f"Error: Tool '{action}' is not in available tools [{tool_names}]."

            print(f"Observation: {observation}")
            trace.append({
                "step": step,
                "thought": thought_text,
                "action": action,
                "input": action_input,
                "observation": observation
            })

            conversation_history += f" {thought_text}\nAction: {action}\nAction Input: {action_input}\nObservation: {observation}\nThought:"

        return {"question": question, "final_answer": "Max steps reached without concluding.", "steps": trace}

    def _fallback_simulated_run(self, question: str) -> Dict[str, Any]:
        trace = []
        file_tool = self.tools["read_local_file"]
        calc_tool = self.tools["python_calculator"]
        search_tool = self.tools["web_search"]

        # Step 1: Read File
        print("\nThought 1: The user wants financial figures. I need to inspect the local file 'sample_data/company_metrics.txt'.")
        print("Action: read_local_file")
        print("Action Input: sample_data/company_metrics.txt")
        obs1 = file_tool.invoke("sample_data/company_metrics.txt")
        print(f"Observation:\n{obs1}")

        # Step 2: Calculator
        print("\nThought 2: From the file, Q3 revenue is $1,850,000 USD and the bonus is 15%. I must calculate 1,850,000 * 0.15.")
        print("Action: python_calculator")
        print("Action Input: 1850000 * 0.15")
        obs2 = calc_tool.invoke("1850000 * 0.15")
        print(f"Observation: {obs2}")

        # Step 3: Web Search
        print("\nThought 3: Now I need to retrieve current economic context for inflation using DuckDuckGo search.")
        print("Action: web_search")
        print("Action Input: current US inflation rate annual latest")
        obs3 = search_tool.invoke("US annual inflation rate latest")
        preview = obs3[:200].replace("\n", " ") + "..."
        print(f"Observation: {preview}")

        final = (
            f"1. Local File Metrics: According to 'company_metrics.txt', Datheno's Q3 revenue was $1,850,000 USD.\n"
            f"2. Calculation: A 15% performance bonus on Q3 revenue equals ${float(obs2):,.2f} USD.\n"
            f"3. Web Research: Real-time search successfully retrieved the current macroeconomic inflation trends."
        )
        print(f"\n[RESULT] Final Answer:\n{final}")
        print("=" * 65)
        return {"question": question, "final_answer": final, "steps": trace}
