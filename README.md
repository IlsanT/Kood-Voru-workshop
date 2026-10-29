# AI under the hood

Slides and demos from a workshop at Kood/Võru, 26-10-2026. How large language
models work, and how to run one on your own laptop with Ollama.

## Slides

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keys: `→` / `←` / space to move, `n` speaker notes, `t` light/dark, `f` fullscreen.

`ai-under-the-hood.pdf` is the same deck as a PDF, without the interactive parts.

## Setup

Install Ollama from https://ollama.com/download, then:

```bash
ollama pull llama3.2:3b
ollama pull llama3.2:1b        # smaller, for 8 GB laptops or slow Wi-Fi
ollama pull nomic-embed-text   # for the embeddings demo
```

## Demos

Run these from this folder. They use only the Python standard library.

| File | What it shows |
|---|---|
| `demos/api.sh` | Ollama is a plain HTTP + JSON API |
| `demos/chat.py` | The model has no memory; the script resends the conversation. Try `--no-memory` |
| `demos/embeddings.py` | Sentences become vectors, and similar meaning scores close to 1 |
| `demos/tools.py` | A tiny agent: the model asks for a tool, the script runs it |

Demo 4 in the slides streams tokens in the browser and talks to Ollama on
`localhost:11434`. If it shows a CORS error, quit Ollama and run
`OLLAMA_ORIGINS="*" ollama serve`.

## License

MIT. Use it however you like.
