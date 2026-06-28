# Testing and CI

This repository uses lightweight CI because the runtime path loads SentenceTransformers, PyTorch, NLTK resources, and an Ollama model.

## Local Validation

Run these checks before opening a pull request:

```bash
python -m compileall app.py database.py prepare_data.py text_similarity.py train.py
python scripts/smoke_check.py
```

For full manual testing:

```bash
pip install -r requirements.txt
ollama create chatub -f Modelfile
python app.py
```

Then send a request to `/ask` from the README example.

## CI Workflow

`.github/workflows/ci.yml` runs on pull requests and pushes to `main`.

The workflow validates:

- Python syntax for the core modules
- required app, frontend, model wrapper, and dependency files
- FAQ JSON structure and required normalized `question` / `answer` fields, including source files that use `q` / `a`

## Current Coverage

The CI workflow intentionally avoids importing `app.py` because import time currently builds embeddings and can download model resources. It also avoids Ollama because the model is a local runtime dependency.

## Recommended Next Tests

- Move embedding training out of module import time.
- Add pure unit tests for Arabic preprocessing and FAQ loading.
- Add an evaluation set for grounded answer quality and no-match behavior.
- Add Flask route tests after the model dependency is injectable or mockable.
