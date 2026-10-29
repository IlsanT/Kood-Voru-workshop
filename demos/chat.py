"""Minimal chat with a local Ollama model.

The model remembers nothing. This script keeps the conversation in a list
and sends the whole list every turn. Run with --no-memory to see it forget.

    python3 chat.py
    python3 chat.py --no-memory
    python3 chat.py --model llama3.2:1b
"""

import argparse
import json
import urllib.request

URL = "http://localhost:11434/api/chat"


def ask(model, messages):
    body = json.dumps({"model": model, "messages": messages, "stream": True}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    reply = ""
    with urllib.request.urlopen(req) as res:
        for line in res:  # one JSON object per line, roughly one token each
            chunk = json.loads(line)
            piece = chunk.get("message", {}).get("content", "")
            print(piece, end="", flush=True)
            reply += piece
    print()
    return reply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="llama3.2:3b")
    parser.add_argument("--no-memory", action="store_true", help="only send the latest message")
    args = parser.parse_args()

    messages = [{"role": "system", "content": "You are a friendly assistant. Keep answers short."}]
    print(f"Chatting with {args.model}. Memory {'OFF' if args.no_memory else 'ON'}. Ctrl+C to quit.\n")

    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue

        messages.append({"role": "user", "content": user})
        to_send = [messages[0], messages[-1]] if args.no_memory else messages
        print(f"[sending {len(to_send)} messages]")
        print("ai> ", end="")
        reply = ask(args.model, to_send)
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
