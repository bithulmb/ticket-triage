# Ticket Triage

An async pipeline that sorts customer support tickets into a category and a priority using an LLM. Answers that can't be validated are flagged for a person instead of crashing the batch.

## How it works

1. `main.py` reads tickets from `tickets.json`.
2. `src/pipeline.py` sends every ticket to the model concurrently (`asyncio.gather`).
3. Each reply is validated with Pydantic:
   - `category` must be `billing`, `shipping` or `other`
   - `priority` must be an integer from 1 (low) to 5 (urgent)
4. Valid replies are marked `checked: true`. Invalid ones get `category: null`, `priority: null`, `checked: false`, and are reported as needing a person.
5. Results are written to `results.json` and logs to `run.log`.

The LLM client in `src/llm.py` uses the OpenAI SDK pointed at Groq's OpenAI-compatible API (model `openai/gpt-oss-120b`). `src/model.py` has a keyword-based mock model for use without an API.

## Project layout

```
main.py            entry point: load tickets, triage, write results
run.py             runs main.py, then prints results.json and run.log
tickets.json       input tickets
src/pipeline.py    Triage schema, triage(), run_all()
src/llm.py         Groq/OpenAI client and ask_model()
src/model.py       mock model (ask_model_mock)
tests/             pytest tests
```

## Setup

Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY=your-key-here
```

## Usage

```bash
python main.py   # writes results.json and run.log
python run.py    # same, and prints both files
```

Input format (`tickets.json`):

```json
[{ "id": 1, "customer": "Asha", "text": "I was charged twice for one order" }]
```

Output format (`results.json`):

```json
[{ "id": 1, "category": "billing", "priority": 4, "checked": true }]
```

## Tests

```bash
pytest
```

`pytest.ini` adds the project root to the import path so `from src...` works.

> Note: `src/llm.py` reads `GROQ_API_KEY` at import time, so it must be set when running the tests too.
