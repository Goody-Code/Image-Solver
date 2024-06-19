from transformers import pipeline

# تحديد النموذج الذي نريد تحميله
model = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

# يمكن تخزين النموذج في ذاكرة التخزين المؤقت
model.save_pretrained('/app/model')
