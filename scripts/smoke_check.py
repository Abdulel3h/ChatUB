from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []

    required_files = [
        "app.py",
        "prepare_data.py",
        "text_similarity.py",
        "index.html",
        "script.js",
        "styles.css",
        "Modelfile",
        "requirements.txt",
    ]

    for relative_path in required_files:
        if not (ROOT / relative_path).is_file():
            errors.append(f"Missing required file: {relative_path}")

    faq_dir = ROOT / "data"
    faq_files = sorted(faq_dir.glob("faq*.json"))
    if not faq_files:
        errors.append("No FAQ JSON files found in data/")

    total_pairs = 0
    for faq_file in faq_files:
        try:
            payload = json.loads(faq_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{faq_file.relative_to(ROOT)} is not valid JSON: {exc}")
            continue

        pairs = payload.get("qa_pairs")
        if not isinstance(pairs, list) or not pairs:
            errors.append(f"{faq_file.relative_to(ROOT)} must contain a non-empty qa_pairs list")
            continue

        for index, pair in enumerate(pairs):
            question = (pair.get("question") or pair.get("q")) if isinstance(pair, dict) else None
            answer = (pair.get("answer") or pair.get("a")) if isinstance(pair, dict) else None
            if not isinstance(question, str) or not question.strip():
                errors.append(f"{faq_file.relative_to(ROOT)} qa_pairs[{index}] is missing question/q text")
            if not isinstance(answer, str) or not answer.strip():
                errors.append(f"{faq_file.relative_to(ROOT)} qa_pairs[{index}] is missing answer/a text")

        total_pairs += len(pairs)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Validated {len(faq_files)} FAQ files with {total_pairs} question-answer pairs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
