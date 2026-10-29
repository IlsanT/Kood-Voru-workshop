"""A tiny agent. The model asks for a tool, this script runs it.

The model never runs code itself. It replies with "call tool X with these
arguments". We run it, send the result back, and the model writes the answer.
Coding agents are this loop with tools like read_file, write_file, run_tests.

Needs a model with tool support, e.g. llama3.2:3b or qwen2.5:7b.

    python3 tools.py "What is 1234 * 5678, and what day is it today?"
"""

import ast
import datetime
import json
import operator
import sys
import urllib.request

URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"


# ---------- Tools: plain Python functions ----------

def get_current_date():
    return datetime.date.today().strftime("%A %d-%m-%Y")


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}


def calculate(expression):
    """Safe arithmetic: numbers and + - * / ** only."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError("unsupported expression")
    return str(ev(ast.parse(expression, mode="eval").body))


TOOLS = {"get_current_date": get_current_date, "calculate": calculate}

# What we tell the model about the tools.
TOOL_SPECS = [
    {"type": "function", "function": {
        "name": "get_current_date",
        "description": "Get today's date",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "Evaluate an arithmetic expression like 12 * (3 + 4)",
        "parameters": {"type": "object", "properties": {
            "expression": {"type": "string", "description": "The expression"}},
            "required": ["expression"]},
    }},
]


# ---------- The loop ----------

def chat(messages):
    body = json.dumps({"model": MODEL, "messages": messages, "tools": TOOL_SPECS, "stream": False}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())["message"]


def main():
    question = " ".join(sys.argv[1:]) or "What is 1234 * 5678, and what day is it today?"
    messages = [{"role": "user", "content": question}]
    print(f"you> {question}\n")

    for _ in range(5):  # safety limit
        msg = chat(messages)
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        if not calls:
            print(f"ai> {msg.get('content', '')}")
            return
        for call in calls:
            name = call["function"]["name"]
            args = call["function"].get("arguments") or {}
            print(f"[model asks: {name}({args})]")
            try:
                result = TOOLS[name](**args)
            except Exception as e:  # show the error to the model, like a real agent would
                result = f"error: {e}"
            print(f"[script runs it: {result}]\n")
            messages.append({"role": "tool", "tool_name": name, "content": result})

    print("Stopped after 5 rounds.")


if __name__ == "__main__":
    main()
