# Reviewer Guide

Use this guide if you are evaluating ChatUB for an AI engineering, LLM applications, or Arabic NLP role.

## 30-Second Review

- Start with `README.md` for the problem, architecture, and setup.
- Open `docs/architecture.md` to see retrieval, context selection, and generation flow.
- Inspect `prepare_data.py`, `text_similarity.py`, and `app.py`.
- Review `data/` to understand the local FAQ knowledge source.

## What This Project Demonstrates

- Arabic-first assistant UX.
- Local AI assistant architecture with Ollama.
- Semantic search over domain-specific knowledge.
- Practical grounding before response generation.
- Honest documentation of evaluation and artifact gaps.

## Quick Technical Path

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

## Prototype Boundaries

- The assistant needs source citations before production use.
- Large generated artifacts should be reviewed before long-term Git storage.
- Answer quality needs an evaluation set and hallucination checks.

## Related Repositories

- [Abdulelah AI Portfolio](https://github.com/Abdulel3h/Abdulelah)
- [architect-of-intelligence](https://github.com/Abdulel3h/architect-of-intelligence)
