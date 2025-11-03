import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def jeydi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Congratulations")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="thank you")

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logging.info(f"User {user.first_name} ({user.id}) said: {update.message.text}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    jeydi_message_handler = MessageHandler(filters.TEXT & filters.Regex(r'(?i)jeydi'), jeydi_handler)
    photo_message_handler = MessageHandler(filters.PHOTO, photo_handler)
    log_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), log_message)
    
    application.add_handler(start_handler)
    application.add_handler(jeydi_message_handler)
    application.add_handler(photo_message_handler)
    # Add the log_handler with a lower group number to run it before other handlers
    application.add_handler(log_handler, group=1)
    
    application.run_polling()
