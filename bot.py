import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from image_processing import extract_text_from_image
from nlp_model import solve_question
from config import TELEGRAM_API_TOKEN, WEBHOOK_URL

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أرسل صورة السؤال الذي تريد حله.')

def handle_image(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1].get_file()
    file_path = f'images/{photo.file_id}.jpg'
    photo.download(file_path)
    
    extracted_text = extract_text_from_image(file_path)
    answer = solve_question(extracted_text)
    
    update.message.reply_text(f'السؤال: {extracted_text}\n\nالحل: {answer}')
    
    os.remove(file_path)  # حذف الصورة بعد المعالجة

def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
    
    # تحديد البورت
    port = int(os.environ.get('PORT', 8080))
    
    # إعدادات الـ Webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=TELEGRAM_API_TOKEN,
                          webhook_url=f"{WEBHOOK_URL}/{TELEGRAM_API_TOKEN}")
    
    updater.bot.set_webhook(f"{WEBHOOK_URL}/{TELEGRAM_API_TOKEN}")
    
    updater.idle()

if __name__ == '__main__':
    main()
