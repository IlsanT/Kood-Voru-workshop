#!/usr/bin/env bash
# Ollama is a local HTTP server. Everything below is plain HTTP + JSON.
# Usage: bash api.sh [model]
MODEL="${1:-llama3.2:3b}"

echo "== Models on this machine =="
curl -s http://localhost:11434/api/tags
echo; echo

echo "== One prompt, one answer =="
curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"Say hi to Kood/Võru in five words.\",
  \"stream\": false
}"
echo; echo

echo "== Chat format: a list of messages =="
curl -s http://localhost:11434/api/chat -d "{
  \"model\": \"$MODEL\",
  \"messages\": [
    {\"role\": \"system\", \"content\": \"Answer in one sentence.\"},
    {\"role\": \"user\", \"content\": \"What is a token?\"}
  ],
  \"stream\": false
}"
echo
