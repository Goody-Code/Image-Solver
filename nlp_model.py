import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import HfApi
from config import HUGGINGFACE_TOKEN, HUGGING_FACE_API_ENDPOINT

api = HfApi()
token = os.getenv("HUGGINGFACE_TOKEN")
api.login(token)

model_name = "EleutherAI/gpt-neox-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def solve_question(question):
    inputs = tokenizer.encode(question, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
