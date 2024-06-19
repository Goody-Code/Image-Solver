import os
from transformers import pipeline
from config import HUGGINGFACE_TOKEN, HUGGING_FACE_API_ENDPOINT

# تهيئة الأنابيب للإجابة على الأسئلة باستخدام النموذج المحمل محليًا
qa_pipeline = pipeline(
    "question-answering", 
    model="/app/model", 
    tokenizer="distilbert-base-uncased-distilled-squad", 
    use_auth_token=HUGGINGFACE_TOKEN,
    api_endpoint=HUGGING_FACE_API_ENDPOINT
)

def generate_response(cleaned_text: str) -> str:
    questions = re.split(r'\d+\.', cleaned_text)
    questions = [q.strip() for q in questions if q.strip()]
    answers = []
    
    for question in questions:
        result = qa_pipeline(question=question, context=cleaned_text)
        answers.append(f"Q: {question}\nA: {result['answer']}")
    
    return "\n\n".join(answers)
