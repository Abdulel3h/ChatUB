from flask import Flask, request, jsonify, send_file
from text_similarity import train_model, generate_custom_answer
from prepare_data import load_all_faqs

app = Flask(__name__)

# تحميل البيانات وتدريب نموذج التشابه عند التشغيل
faqs = load_all_faqs()
model_data = train_model(faqs)
context = {}

@app.route('/')
def serve_frontend():
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_file(path)
    except FileNotFoundError:
        return "", 404

@app.route('/ask', methods=['POST'])
def ask_question():
    global model_data, context

    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'answer': 'أدخل سؤالًا من فضلك.'}), 200, {'Content-Type': 'application/json; charset=utf-8'}

    # توليد إجابة دائمًا باستخدام النموذج
    answer = generate_custom_answer(question, model_data, context, max_words=50)

    # حفظ السياق
    context["last_question"] = question
    context["last_answer"] = answer

    return jsonify({'answer': answer}), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    print("🚀 السيرفر يعمل على http://127.0.0.1:5000")
    app.run(debug=True)
