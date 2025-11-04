import logging
import os
import requests
import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id='665633939', text='One message every minute')

async def send_weather_forecast(context: ContextTypes.DEFAULT_TYPE):
    """Fetches and sends the daily weather forecast for Lubumbashi."""
    lat = -11.66
    lon = 27.48
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Africa/Lubumbashi"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Assuming the API returns daily data for today
        today_forecast = data['daily']
        weather_code = today_forecast['weathercode'][0]
        max_temp = today_forecast['temperature_2m_max'][0]
        min_temp = today_forecast['temperature_2m_min'][0]

        message = (
            f"🌤️ **Prévisions météo pour Lubumbashi**\n\n"
            f"🌡️ Température maximale: {max_temp}°C\n"
            f"❄️ Température minimale: {min_temp}°C\n"
            f"🛰️ Météo: {get_weather_description(weather_code)}"
        )
        
        # Replace with your target chat ID
        await context.bot.send_message(chat_id='665633939', text=message)
    except Exception as e:
        logging.error(f"Error fetching weather forecast: {e}")

def get_weather_description(code):
    # Weather codes from Open-Meteo documentation
    weather_codes = {
        0: "Ciel clair",
        1: "Principalement clair",
        2: "Partiellement nuageux",
        3: "Couvert",
        45: "Brouillard",
        48: "Brouillard givrant",
        51: "Bruine légère",
        53: "Bruine modérée",
        55: "Bruine dense",
        56: "Bruine verglaçante légère",
        57: "Bruine verglaçante dense",
        61: "Pluie légère",
        63: "Pluie modérée",
        65: "Pluie forte",
        66: "Pluie verglaçante légère",
        67: "Pluie verglaçante forte",
        71: "Chute de neige légère",
        73: "Chute de neige modérée",
        75: "Chute de neige forte",
        77: "Grains de neige",
        80: "Averses de pluie légères",
        81: "Averses de pluie modérées",
        82: "Averses de pluie violentes",
        85: "Averses de neige légères",
        86: "Averses de neige fortes",
        95: "Orage",
        96: "Orage avec grêle légère",
        99: "Orage avec grêle forte",
    }
    return weather_codes.get(code, "Inconnue")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def jeydi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Congratulations")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="thank you")

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id
    logging.info(f"User {user.first_name} ({user.id}) in chat {chat_id} said: {update.message.text}")

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
    
    # Schedule the weather forecast to be sent every day at 8:00 AM
    application.job_queue.run_daily(
        callback=send_weather_forecast,
        time=datetime.time(hour=8, minute=0),
        days=(0, 1, 2, 3, 4, 5, 6)
    )
    
    application.run_polling()
