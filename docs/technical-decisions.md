# Technical Decisions

| Decision | Rationale | Tradeoff |
| --- | --- | --- |
| Use local FAQ JSON files | Keeps the prototype reviewable without external services. | Knowledge updates require data-file maintenance. |
| Use SentenceTransformers | Provides semantic matching across user questions and FAQ content. | Startup and memory cost can rise with larger datasets. |
| Use Ollama for generation | Supports local AI experimentation and privacy-aware behavior. | Reviewers need Ollama installed to reproduce full behavior. |
| Keep Flask API small | Makes the prototype easy to run and inspect. | Production concerns such as auth, observability, and scaling are not included yet. |
