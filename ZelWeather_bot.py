import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

# Получаем ключи из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = 'Zelenograd, RU'

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для преобразования времени из UNIX в нормальный формат
def format_unix_time(unix_time, tz_shift):
    dt = datetime.utcfromtimestamp(unix_time + tz_shift)
    return dt.strftime("%H:%M")

# Команда /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description'].capitalize()
        sunrise = format_unix_time(data['sys']['sunrise'], data['timezone'])
        sunset = format_unix_time(data['sys']['sunset'], data['timezone'])
        dt = datetime.utcfromtimestamp(data['dt'] + data['timezone']).strftime("%d.%m.%Y %H:%M")

        weather_message = (
            f"🌤 Погода в Зеленограде ({dt}):\n"
            f"Описание: {description}\n"
            f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"Влажность: {humidity}%\n"
            f"Ветер: {wind_speed} м/с\n"
            f"🌅 Восход: {sunrise}\n"
            f"🌇 Закат: {sunset}"
        )

        await update.message.reply_text(weather_message)
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
