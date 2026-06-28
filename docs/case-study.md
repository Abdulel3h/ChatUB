# Case Study

## Context

ChatUB is a local Arabic academic assistant prototype for University of Bisha students. It combines local FAQ data, multilingual embeddings, similarity search, and Ollama generation.

## Problem

Students need quick answers to academic questions, but generic chatbots can answer without trusted university context. The project explores a more constrained assistant that starts from local academic content.

## Constraints

- The assistant should run locally for privacy-aware review.
- Arabic preprocessing and retrieval quality need explicit evaluation.
- Ollama availability cannot be assumed in every reviewer environment.
- The project must not claim production deployment or verified answer quality.

## Solution

The Flask app loads local FAQ JSON files, builds embeddings with SentenceTransformers, selects a close reference answer, and sends a compact Arabic prompt to an Ollama model wrapper. The browser UI calls `/ask` and displays the generated answer.

## Architecture

See [Architecture](architecture.md). The core flow is local FAQ data -> preprocessing -> embeddings -> nearest context -> generated Arabic response.

## Key Engineering Decisions

- Keep university content local.
- Use semantic similarity before generation to reduce generic answers.
- Keep answer length constrained.
- Make Flask debug mode opt-in through `FLASK_DEBUG`.
- Serve static assets through Flask's safe directory helper instead of raw file paths.

## Trade-Offs

- Embedding generation at startup simplifies the prototype but slows first run.
- Local model execution improves privacy but depends on Ollama setup.
- Current retrieval has no source citations, so production use would need stronger grounding.

## What I Learned

- Arabic assistant quality depends heavily on preprocessing, trusted source data, and fallback behavior.
- Local AI demos still need production-style security defaults.

## Current Limitations

- No automated evaluation set for answer correctness or hallucination risk.
- No source citations in responses.
- Model artifacts and generated checkpoints should be reviewed before long-term Git storage.

## Future Improvements

- Precompute embeddings.
- Add citation-aware responses.
- Add tests for `/ask`, empty questions, and no-match fallbacks.
- Document the exact source provenance for each FAQ file.

## Reviewer Evaluation

Inspect `prepare_data.py`, `text_similarity.py`, `app.py`, `Modelfile`, and `data/`. Evaluate the retrieval path, local-model assumptions, Arabic UX, and documented prototype boundaries.
