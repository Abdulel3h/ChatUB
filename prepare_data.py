import json
import os

def load_all_faqs():
    all_faqs = []
    for i in range(1, 8):  # faq1 إلى faq7
        path = f"data/faq{i}.json"
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # افترض وجود "qa_pairs" في كل JSON
                if "qa_pairs" in data:
                    for item in data["qa_pairs"]:
                        question = item.get("question") or item.get("q")
                        answer = item.get("answer") or item.get("a")
                        if question and answer:
                            all_faqs.append({
                                "question": question,
                                "answer": answer,
                            })
    return all_faqs
