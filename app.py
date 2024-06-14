import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from image_processing import extract_text_from_image
from nlp_model import solve_question
from config import TELEGRAM_API_TOKEN, WEBHOOK_URL

app = Flask(__name__)
bot = Bot(token=TELEGRAM_API_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def start(update, context):
    update.message.reply_text('أرسل صورة السؤال الذي تريد حله.')

def handle_image(update, context):
    photo = update.message.photo[-1].get_file()
    file_path = f'images/{photo.file_id}.jpg'
    photo.download(file_path)
    
    extracted_text = extract_text_from_image(file_path)
    answer = solve_question(extracted_text)
    
    update.message.reply_text(f'السؤال: {extracted_text}\n\nالحل: {answer}')
    
    os.remove(file_path)  # حذف الصورة بعد المعالجة

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    from os import environ
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
