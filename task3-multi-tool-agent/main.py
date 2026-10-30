import argparse
import sys
from agent import ResearchAgentExecutor


def main():
    parser = argparse.ArgumentParser(
        description="Task 3: Autonomous Multi-Tool AI Research Agent (LangChain + DuckDuckGo)"
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Compound query for the research agent to solve"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run an interactive session where you can prompt the agent repeatedly"
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        default="gemini",
        help="LLM provider (default: gemini)"
    )

    args = parser.parse_args()
    agent = ResearchAgentExecutor(provider=args.provider)

    if args.interactive:
        print("Starting interactive agent mode. Type 'exit' to quit.\n")
        while True:
            try:
                user_q = input("\nEnter query for agent: ").strip()
                if user_q.lower() in ["exit", "quit"]:
                    break
                if not user_q:
                    continue
                agent.run(user_q)
            except KeyboardInterrupt:
                break
    elif args.query:
        agent.run(args.query)
    else:
        # Default test compound query
        default_query = (
            "Read 'sample_data/company_metrics.txt', find the Q3 revenue, calculate a 15% bonus, "
            "and search DuckDuckGo for the latest inflation figures."
        )
        print(f"No --query provided. Running default multi-tool compound query:\n\"{default_query}\"\n")
        agent.run(default_query)


if __name__ == "__main__":
    main()
