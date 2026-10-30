import re
import ast
import operator
from pathlib import Path
from typing import Union
from duckduckgo_search import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Search the web in real-time using DuckDuckGo.
    Use this tool to find up-to-date facts, current events, population numbers, or general web data.
    Input should be a concise search query string.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                title = r.get("title", "")
                snippet = r.get("body", "")
                link = r.get("href", "")
                results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {link}")

        if not results:
            return "No web results found for the query."
        return "\n\n---\n\n".join(results)
    except Exception as e:
        return f"Error executing web search: {str(e)}"


# Safe mathematical evaluator without eval()
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}

def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    raise ValueError(f"Unsupported expression element: {type(node)}")


@tool
def python_calculator(expression: str) -> str:
    """
    Safely calculates mathematical expressions.
    Input must be a valid mathematical formula like '1850000 * 0.15', '(45 + 28) / 2', or '10 ** 3'.
    Do not pass descriptive text into this tool, only math formulas.
    """
    try:
        # Clean string
        cleaned = expression.strip().replace("$", "").replace(",", "")
        parsed = ast.parse(cleaned, mode="eval")
        result = _eval_node(parsed.body)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"


@tool
def read_local_file(file_path: str) -> str:
    """
    Reads the full content of a local file.
    Input must be a relative or absolute file path (e.g. 'sample_data/company_metrics.txt').
    """
    try:
        p = Path(file_path.strip().strip("'").strip('"'))
        if not p.exists():
            return f"Error: File '{file_path}' does not exist on disk."
        if not p.is_file():
            return f"Error: Path '{file_path}' is not a regular file."
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"


def get_all_tools():
    """Returns list of LangChain tools available for the agent."""
    return [web_search, python_calculator, read_local_file]
