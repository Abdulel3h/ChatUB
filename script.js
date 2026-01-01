function sendQuestion() {
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    const chatBox = document.getElementById('chatBox');

    if (question === '') return;

    // عرض سؤال المستخدم
    const userMsg = document.createElement('div');
    userMsg.className = 'message user-message';
    userMsg.textContent = question;
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    // عرض رسالة تحميل
    const loading = document.createElement('div');
    loading.className = 'message bot-message loading';
    loading.textContent = 'جارٍ التحميل...';
    loading.dir = 'rtl';
    chatBox.appendChild(loading);
    chatBox.scrollTop = chatBox.scrollHeight;

    // إرسال السؤال
    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({ question })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        loading.remove();

        const botMsg = document.createElement('div');
        botMsg.className = 'message bot-message';
        botMsg.textContent = data.answer || 'عذرًا، لا توجد إجابة.';
        botMsg.dir = 'rtl';
        chatBox.appendChild(botMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        loading.remove();
        const errorMsg = document.createElement('div');
        errorMsg.className = 'message bot-message';
        errorMsg.textContent = 'عذرًا، حدث خطأ أو النموذج غير جاهز. حاول تشغيل `ollama run chatub`.';
        errorMsg.dir = 'rtl';
        chatBox.appendChild(errorMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
        console.error('Error:', error);
    });

    input.value = '';
}

// إرسال بالـ Enter
document.getElementById('questionInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendQuestion();
});
