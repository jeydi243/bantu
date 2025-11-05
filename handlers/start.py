from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db import crud

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    db: Session = next(SessionLocal())
    
    crud.get_or_create_user(
        db=db,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
