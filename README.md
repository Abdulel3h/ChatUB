<p align="center">
  <img src="./assets/project-banner.svg" alt="ChatUB project banner" />
</p>

# ChatUB - Local AI Academic Assistant

ChatUB is a local AI academic assistant prototype for University of Bisha students. It answers Arabic academic questions using local FAQ data, multilingual sentence embeddings, similarity search, and an Ollama-served generation model.

## Overview

The project explores how a university-specific assistant can provide more useful answers than a generic chatbot by grounding responses in official academic question-answer content. It is a graduation-project style prototype focused on Arabic UX, local knowledge, and privacy-aware AI behavior.

## Documentation

- [Architecture](docs/architecture.md)
- [Case Study](docs/case-study.md)
- [Engineering Principles](docs/engineering-principles.md)
- [Technical Decisions](docs/technical-decisions.md)
- [Reviewer Guide](docs/reviewer-guide.md)

## Features

- Arabic web chat interface
- Flask API endpoint for questions
- FAQ loading from local JSON files
- Arabic preprocessing with NLTK stop words
- SentenceTransformer embeddings for semantic matching
- Ollama integration for generated Arabic answers
- Basic conversation context for the latest question and answer

## Architecture

```text
User browser
  -> Flask app.py
  -> prepare_data.py loads FAQ JSON files
  -> text_similarity.py builds multilingual embeddings
  -> nearest FAQ answer is selected as reference context
  -> Ollama model "chatub" generates a concise Arabic response
```

## Tech Stack

- Python
- Flask
- SentenceTransformers
- PyTorch
- NLTK
- Ollama
- HTML, CSS, JavaScript
- Local JSON FAQ data

## Installation

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
ollama create chatub -f Modelfile
python app.py
```

Open `http://127.0.0.1:5000`.

Optional local environment:

```bash
FLASK_DEBUG=0
```

## Usage

Send a POST request to `/ask`:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"ما شروط الاعتذار عن مقرر؟\"}"
```

## Screenshots

![ChatUB chat interface](assets/screenshots/chatub-home.png)

Captured from the committed static chat interface. Add a grounded answer flow after the local model and FAQ evaluation set are ready.

## System Design

- `app.py` serves the frontend and `/ask` API.
- `prepare_data.py` loads university FAQ files.
- `text_similarity.py` preprocesses Arabic text, creates embeddings, and selects relevant context.
- `Modelfile` defines the local Ollama model wrapper.
- `data/` stores local FAQ JSON files.
- `trained_model/` and `results/` contain generated model artifacts and should be reviewed before keeping them in Git.

## Folder Structure

```text
app.py                 Flask server and API route
index.html             Chat UI
script.js              Browser interaction logic
styles.css             Chat styling
data/                  FAQ JSON files
trained_model/         Model/tokenizer artifacts
results/               Training checkpoint artifacts
Modelfile              Ollama model definition
```

## Challenges

- Arabic preprocessing and answer quality require careful evaluation.
- Large model artifacts and checkpoints increase repository size.
- The current app trains embeddings on startup, which can slow first response.
- There is no automated evaluation set for answer accuracy or hallucination behavior.

## Future Work

- Add source citations to every response.
- Move embedding generation to an offline build step.
- Add tests for `/ask`, preprocessing, and no-match fallback behavior.
- Add grounded-answer screenshots and a demo video after evaluation is ready.
- Document the exact official university sources used in `data/`.
- Review committed model artifacts and remove generated files that are not needed.

## License

No license file is currently present. All rights are reserved by default unless a license is added.

## Author

Abdulelah Alkhathami

## Contact

- Website: [abdulelah.de](https://www.abdulelah.de)
- GitHub: [Abdulel3h](https://github.com/Abdulel3h)
