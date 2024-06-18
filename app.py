import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from config import TELEGRAM_TOKEN
from image_processing import process_image

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return 'ok'

def start(update, context):
    update.message.reply_text('مرحبًا! أرسل لي صورة تحتوي على الأسئلة أو التمارين.')

def handle_image(update, context):
    photo_file = update.message.photo[-1].get_file()
    response_text = process_image(photo_file)
    update.message.reply_text(response_text)

dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8443))
    app.run(host='0.0.0.0', port=port)
