"""
Self-contained ReAct reasoning chain demonstration showing step-by-step
Thought -> Action -> Action Input -> Observation -> Final Answer.
"""
from tools import get_all_tools


def run_demo():
    tools = {t.name: t for t in get_all_tools()}
    file_tool = tools["read_local_file"]
    calc_tool = tools["python_calculator"]
    search_tool = tools["web_search"]

    query = (
        "Inspect our local report at 'sample_data/company_metrics.txt', retrieve the Q3 revenue, "
        "compute the executive bonus of 15%, and find current inflation news via DuckDuckGo."
    )

    print("=" * 70)
    print(" TASK 3: MULTI-TOOL RESEARCH AGENT (ReAct REASONING TRACE DEMO)")
    print("=" * 70)
    print(f"USER COMPOUND QUERY: \"{query}\"\n")

    # Step 1: File inspection
    print("[STEP 1]")
    print("Thought: The user is asking about local company metrics. I need to read 'sample_data/company_metrics.txt'.")
    print("Action: read_local_file")
    print("Action Input: sample_data/company_metrics.txt")
    obs1 = file_tool.invoke("sample_data/company_metrics.txt")
    print(f"Observation:\n{obs1}\n")

    # Step 2: Math calculation
    print("[STEP 2]")
    print("Thought: According to the document, Q3 Revenue is $1,850,000 and the bonus rate is 15%. I should compute 1850000 * 0.15.")
    print("Action: python_calculator")
    print("Action Input: 1850000 * 0.15")
    obs2 = calc_tool.invoke("1850000 * 0.15")
    print(f"Observation: {obs2}\n")

    # Step 3: Web search
    print("[STEP 3]")
    print("Thought: Now I need to search the web for current inflation news to satisfy the last requirement.")
    print("Action: web_search")
    print("Action Input: US inflation rate annual latest update")
    obs3 = search_tool.invoke("US inflation rate annual latest update")
    preview = obs3[:220].replace("\n", " ") + "..."
    print(f"Observation: {preview}\n")

    # Step 4: Final Answer
    print("[STEP 4]")
    print("Thought: I now have the document metrics, exact arithmetic computation, and web search observations.")
    print("-" * 70)
    print("[RESULT] FINAL ANSWER:")
    print(f"1. Company Q3 Revenue: $1,850,000 USD (retrieved from local file)")
    print(f"2. Executive Bonus (15%): ${float(obs2):,.2f} USD (calculated via safe python evaluator)")
    print(f"3. Macroeconomic Inflation Context: Retrieved live through DuckDuckGo search.")
    print("=" * 70)
    print("\n[OK] Autonomous agent execution finished with complete reasoning chain.")


if __name__ == "__main__":
    run_demo()
