from multiprocessing import util

import torch

from text_similarity import preprocess_text


def generate_with_llama(prompt):
    import subprocess
    try:
        result = subprocess.run(
            ["ollama", "run", "chatub", prompt],
            capture_output=True,
            text=True,
            timeout=180
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "عذرًا، لا أستطيع توليد الإجابة الآن. يرجى مراجعة مرشدك الأكاديمي."
    except Exception as e:
        print("❌ Ollama error:", e)
        return "حدث خطأ أثناء توليد الإجابة."

def find_closest_answer(user_question, model_data, context=None):
    faqs = model_data["faqs"]
    embeddings = model_data["embeddings"]
    model = model_data["model"]

    user_input = preprocess_text(user_question)
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    cos_scores = util.cos_sim(user_embedding, embeddings)[0]
    top_score, top_idx = torch.max(cos_scores, dim=0)
    top_score = top_score.item()
    print(f"🔍 Similarity Score: {top_score:.3f}")

    if top_score > 0.7:
        answer = faqs[top_idx]["answer"]
        if context is not None:
            context["last_question"] = user_question
            context["last_answer"] = answer
        return f"بناءً على سؤالك: {answer}"

    # إذا لم يوجد تطابق كاف → استدعاء التوليد
    prompt = f"السؤال: {user_question}\nأجب بالعربية الفصحى وبأسلوب أكاديمي."
    return generate_with_llama(prompt)
