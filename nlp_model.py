import os
from transformers import pipeline

token = os.getenv("HUGGINGFACE_TOKEN")

# تهيئة الأنابيب للإجابة على الأسئلة
qa_pipeline = pipeline("question-answering", model="EleutherAI/gpt-neo-1.3B", tokenizer="EleutherAI/gpt-neo-1.3B", use_auth_token=token)

def generate_response(cleaned_text: str) -> str:
    questions = re.split(r'\d+\.', cleaned_text)
    questions = [q.strip() for q in questions if q.strip()]
    answers = []
    
    for question in questions:
        result = qa_pipeline(question=question, context=cleaned_text)
        answers.append(f"Q: {question}\nA: {result['answer']}")
    
    return "\n\n".join(answers)
