import json
import os

def init_db():
    # إنشاء قاعدة بيانات فارغة أو أي تهيئة
    pass

def get_all_faqs():
    qa_pairs = []
    for i in range(1, 8):
        file_path = f'data/faq{i}.json'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if "qa_pairs" in data:
                    qa_pairs.extend(data["qa_pairs"])
                else:
                    print(f"⚠️ {file_path} لا يحتوي على 'qa_pairs'")
    return qa_pairs
