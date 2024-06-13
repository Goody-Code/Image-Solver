import logging
from io import BytesIO
from PIL import Image
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from transformers import GPTNeoForCausalLM, AutoTokenizer
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# إعداد التسجيلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# إعداد Azure OCR
subscription_key = '2444bfedecf34964abbfed9c7112e7ff'
endpoint = 'https://imagesbotsolver.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# تحميل النموذج والمحول
model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'photo':
        # استقبال الصورة
        file_id = msg['photo'][-1]['file_id']
        file_path = bot.getFile(file_id)['file_path']
        image_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"

        # تحميل الصورة ومعالجتها
        image_data = requests.get(image_url).content
        image = Image.open(BytesIO(image_data))

        # استخدام Azure OCR لاستخراج النص من الصورة
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        ocr_results = computervision_client.read_in_stream(BytesIO(image_bytes), raw=True)
        operation_location = ocr_results.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # انتظار النتائج
        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break

        if result.status == OperationStatusCodes.succeeded:
            text = ""
            for text_result in result.analyze_result.read_results:
                for line in text_result.lines:
                    text += line.text + " "
        else:
            bot.sendMessage(chat_id, 'حدث خطأ أثناء قراءة النص من الصورة.')
            return

        # استخدام النموذج للإجابة على الأسئلة
        inputs = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
        reply_ids = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)

        bot.sendMessage(chat_id, reply)

# تكوين البوت
API_TOKEN = '7150721411:AAFRM5keUChtTDJgTGlyeYG6qTrKwHOWjnA'
bot = telepot.Bot(API_TOKEN)
MessageLoop(bot, handle).run_as_thread()

print('Listening ...')

while True:
    pass
