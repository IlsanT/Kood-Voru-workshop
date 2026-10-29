"""Turn sentences into vectors and compare them.

Needs: ollama pull nomic-embed-text

    python3 embeddings.py
    python3 embeddings.py "I like cats" "Dogs are great" "Taxes are due"
"""

import json
import math
import sys
import urllib.request

URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"

DEFAULT_SENTENCES = [
    "I love my dog",
    "My puppy is the best",
    "The stock market fell today",
    "Tallinn is the capital of Estonia",
    "Estonia's main city is Tallinn",
]


def embed(texts):
    body = json.dumps({"model": MODEL, "input": texts}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())["embeddings"]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def main():
    sentences = sys.argv[1:] or DEFAULT_SENTENCES
    vectors = embed(sentences)

    print(f"Each sentence is now a list of {len(vectors[0])} numbers.")
    print("First 5 numbers of sentence 1:", [round(x, 3) for x in vectors[0][:5]])
    print("\nSimilarity (1.0 = same meaning):\n")

    labels = [f"{i + 1}" for i in range(len(sentences))]
    for i, s in enumerate(sentences):
        print(f"  {labels[i]}. {s}")
    print("\n      " + "".join(f"{l:>7}" for l in labels))
    for i, a in enumerate(vectors):
        row = "".join(f"{cosine(a, b):7.2f}" for b in vectors)
        print(f"  {labels[i]:>3} {row}")


if __name__ == "__main__":
    main()
