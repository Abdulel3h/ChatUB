# ChatUB · Local Arabic Academic Assistant · Overview

> The full project overview. The [README](../README.md) is the short version; this page keeps every detail.


An Arabic academic assistant that answers university questions from local FAQ data and a locally served model, so the knowledge and the inference both stay on the machine that runs it.

**Status: prototype.** A graduation-project style prototype built around University of Bisha academic content. It has no automated answer-quality evaluation and is not deployed for students.

## Problem

A generic chatbot does not know a specific university's rules. Students asking in Arabic about course withdrawal, apology deadlines or registration get confident answers that are not grounded in their own institution's published content — and sending those questions to a hosted model means sending campus questions off-site.

## Solution

ChatUB keeps a curated set of academic question–answer pairs in the repository, matches an incoming Arabic question against them with multilingual sentence embeddings, and passes the closest entry to a locally served model as reference context. The answer is generated in Arabic, on the same machine.

## How it works

1. **Load the local knowledge.** `prepare_data.py` reads the FAQ JSON files in `data/`.
2. **Prepare the Arabic text.** `text_similarity.py` preprocesses the question, removing NLTK Arabic stop words.
3. **Match by meaning, not keywords.** Multilingual SentenceTransformer embeddings select the nearest FAQ entry as reference context.
4. **Generate locally.** The Ollama model defined in `Modelfile` produces a concise Arabic response using that context.
5. **Keep a little continuity.** The latest question and answer are carried as conversation context.

## Architecture

```text
User browser
  -> Flask app.py
  -> prepare_data.py loads FAQ JSON files
  -> text_similarity.py builds multilingual embeddings
  -> nearest FAQ answer is selected as reference context
  -> Ollama model "chatub" generates a concise Arabic response
```

## Verified capabilities

These are implemented and readable in the source; none is a measured quality result.

| Capability | Where it lives |
|---|---|
| Arabic web chat interface | `index.html`, `script.js`, `styles.css` |
| `/ask` JSON endpoint | `app.py` |
| Local FAQ loading | `prepare_data.py`, `data/*.json` |
| Arabic preprocessing with stop words | `text_similarity.py` |
| Semantic matching via sentence embeddings | `text_similarity.py` |
| Local generation wrapper | `Modelfile` |

## Screenshot

![ChatUB chat interface](../assets/screenshots/chatub-home.png)

Captured from the committed static chat interface.

## Tech stack

Python · Flask · SentenceTransformers · PyTorch · NLTK · Ollama

## Quick start

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
ollama create chatub -f Modelfile
python app.py
```

Open `http://127.0.0.1:5000`, then ask a question directly:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"ما شروط الاعتذار عن مقرر؟\"}"
```

## Limitations

- **Grounding is not guaranteed.** When no FAQ passes the similarity threshold, generation can continue without reference context.
- **No automated evaluation.** There is no test set for answer accuracy or hallucination behaviour, so no quality number is claimed.
- **Startup cost.** FAQ embeddings are computed when the app starts; this is not model training.
- **Repository weight.** Committed model and checkpoint artifacts make the repository large and should be reviewed.
- **Sources.** The exact official university sources behind `data/` are not yet documented in the repository.

## Repository structure

```text
app.py                 Flask server and /ask route
index.html             Chat UI
script.js              Browser interaction logic
styles.css             Chat styling
data/                  FAQ JSON files
trained_model/         Model/tokenizer artifacts
results/               Training checkpoint artifacts
Modelfile              Ollama model definition
```

## Documentation

[Architecture](architecture.md) · [Case study](case-study.md) · [Engineering principles](engineering-principles.md) · [Technical decisions](technical-decisions.md) · [Reviewer guide](reviewer-guide.md)

## License

No license file is currently present. All rights are reserved by default unless a license is added.

## Contact

**Abdulelah Alkhathami** · [Portfolio](https://abdulelah.de) · [GitHub](https://github.com/Abdulel3h) · [Email](mailto:me@abdulelah.de)
