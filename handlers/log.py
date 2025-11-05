import logging
from telegram import Update
from telegram.ext import ContextTypes

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id
    logging.info(f"User {user.first_name} ({user.id}) in chat {chat_id} said: {update.message.text}")
