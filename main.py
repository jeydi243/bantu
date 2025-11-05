import logging
import os
import requests
import datetime
from dotenv import load_dotenv
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from db.database import engine
from db.models import Base
from handlers.start import start
from handlers.jeydi import jeydi_handler
from handlers.photo import photo_handler
from handlers.log import log_message

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def init_db():
    Base.metadata.create_all(bind=engine)

async def send_weather_forecast(context: ContextTypes.DEFAULT_TYPE):
    """Fetches and sends the daily weather forecast for Lubumbashi."""
    lat = -11.66
    lon = 27.48
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Africa/Lubumbashi"
    
    try:
        response = requests.get(url)
        data = response.json()
        
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
        
        await context.bot.send_message(chat_id='665633939', text=message)
    except Exception as e:
        logging.error(f"Error fetching weather forecast: {e}")

def get_weather_description(code):
    weather_codes = {
        0: "Ciel clair", 1: "Principalement clair", 2: "Partiellement nuageux", 3: "Couvert",
        45: "Brouillard", 48: "Brouillard givrant", 51: "Bruine légère", 53: "Bruine modérée",
        55: "Bruine dense", 56: "Bruine verglaçante légère", 57: "Bruine verglaçante dense",
        61: "Pluie légère", 63: "Pluie modérée", 65: "Pluie forte", 66: "Pluie verglaçante légère",
        67: "Pluie verglaçante forte", 71: "Chute de neige légère", 73: "Chute de neige modérée",
        75: "Chute de neige forte", 77: "Grains de neige", 80: "Averses de pluie légères",
        81: "Averses de pluie modérées", 82: "Averses de pluie violentes", 85: "Averses de neige légères",
        86: "Averses de neige fortes", 95: "Orage", 96: "Orage avec grêle légère", 99: "Orage avec grêle forte",
    }
    return weather_codes.get(code, "Inconnue")

if __name__ == '__main__':
    init_db()
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    jeydi_message_handler = MessageHandler(filters.TEXT & filters.Regex(r'(?i)jeydi'), jeydi_handler)
    photo_message_handler = MessageHandler(filters.PHOTO, photo_handler)
    log_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), log_message)
    
    application.add_handler(start_handler)
    application.add_handler(jeydi_message_handler)
    application.add_handler(photo_message_handler)
    application.add_handler(log_handler, group=1)
    
    if application.job_queue is not None:  
        application.job_queue.run_daily(
            callback=send_weather_forecast,
            time=datetime.time(hour=8, minute=0),
            days=tuple(range(7))
        )
    
    application.run_polling()

