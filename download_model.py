# download_model.py
from transformers import pipeline

# تحديد النموذج الذي نريد تحميله
model = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
