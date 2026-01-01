import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer, util
import torch
import subprocess
import re

# تحميل موارد NLTK
try:
    nltk.data.find('stopwords')
    nltk.data.find('punkt')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

# ======== تحميل نموذج التشابه ========
print("📘 Loading embedding model...")
embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# ======== إعداد كلمات التوقف ========
arabic_stopwords = set(stopwords.words('arabic'))
custom_stopwords = ['وش', 'هل', 'كيف', 'متى', 'من', 'عن', 'في', 'على']
stop_words = arabic_stopwords.union(custom_stopwords)

# ======== تنظيف النص ========
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [w for w in tokens if w.isalnum() and w not in stop_words]
    return ' '.join(filtered_tokens)

# ======== البحث عن أقرب إجابة ========
def find_closest_answer(user_question, model_data):
    faqs = model_data["faqs"]
    embeddings = model_data["embeddings"]
    model = model_data["model"]

    user_input = preprocess_text(user_question)
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    cos_scores = util.cos_sim(user_embedding, embeddings)[0]
    top_score, top_idx = torch.max(cos_scores, dim=0)
    top_score = top_score.item()
    print(f"🔍 Similarity Score: {top_score:.3f}")

    if top_score > 0.5:
        return faqs[top_idx]["answer"]  # فقط كمصدر مرجعي
    return None

# ======== تنظيف إجابات النموذج ========
def clean_answer(answer):
    # الاحتفاظ بالعربية وبعض الرموز
    clean = re.sub(r"[^\u0600-\u06FF0-9.,!?()٪\- ]+", "", answer)
    return clean.strip()

# ======== توليد الإجابة باستخدام ollama ========
def generate_custom_answer(question, model_data, context=None, max_words=50):
    try:
        reference_answer = find_closest_answer(question, model_data)
        reference_text = f"استخدم هذه المعلومات كمصدر فقط: {reference_answer}" if reference_answer else ""

        # برومبت مختصر
        prompt = f"{reference_text}\nالسؤال: {question}\nأجب باختصار وباللغة العربي وبشكل أكاديمي، أقصى {max_words} كلمة."

        # إرسال البرومبت للنموذج عبر stdin لتجنب مشاكل الطول والترميز
        result = subprocess.run(
            ["ollama", "run", "chatub"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30  # زمن أقصى أقصر لتقليل انتظار طويل
        )

        answer = result.stdout.strip()
        if not answer:
            return "عذرًا، لا أستطيع توليد إجابة في الوقت الحالي."
        return answer
    except subprocess.TimeoutExpired:
        return "عذرًا، استغرق النموذج وقتًا طويلاً للرد."
    except Exception as e:
        print("❌ Ollama error:", e)  # يمكن الاحتفاظ بالخطأ بدون البرومبت
        return "حدث خطأ أثناء توليد الإجابة."


# ======== تدريب نموذج التشابه ========
def train_model(faqs):
    clean_faqs = [qa for qa in faqs if "question" in qa and "answer" in qa]
    questions = [preprocess_text(qa["question"]) for qa in clean_faqs]
    embeddings = embedding_model.encode(questions, convert_to_tensor=True, show_progress_bar=True)
    return {"faqs": clean_faqs, "embeddings": embeddings, "model": embedding_model}
