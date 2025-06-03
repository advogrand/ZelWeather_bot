import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем ключи из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = 'Zelenograd, RU'

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        await update.message.reply_text(f"Погода в Зеленограде:\n{description.capitalize()}, {temp}°C")
    else:
        await update.message.reply_text("Не удалось получить погоду :(")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /weather чтобы узнать погоду в Зеленограде.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    app.run_polling()

if __name__ == '__main__':
    main()
