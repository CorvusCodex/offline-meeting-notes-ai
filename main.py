#!/usr/bin/env python3
"""
Meeting Notes Generator (offline)
Usage:
  python main.py --file transcript.txt
  python main.py --input "Transcript..."
"""
import argparse, requests, os, sys

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "llama3.2:4b"
TIMEOUT = 600

def run_llama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def build_prompt(transcript):
    return (
        "You are a meeting summarizer. Produce:\n"
        "- Key decisions (bullet list)\n"
        "- Action items (format: Owner - Task - Deadline)\n"
        "- Risks / Blockers\n"
        "- Short executive summary (1-2 sentences)\n\n"
        f"TRANSCRIPT:\n{transcript}\n\nRespond in plain text with clear sections."
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f")
    p.add_argument("--input", "-i")
    args = p.parse_args()
    content = args.input or ""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                content = (content + "\n" if content else "") + fh.read()
        except Exception as e:
            print("Error:", e, file=sys.stderr); sys.exit(1)
    if not content.strip(): print("Provide --input or --file", file=sys.stderr); sys.exit(1)
    print(run_llama(build_prompt(content)))

if __name__ == "__main__":
    main()
