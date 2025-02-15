from telegram import Update
from telegram.ext import CommandHandler
from services.openweather import get_weather

async def weather(update: Update, context) -> None:
    city = " ".join(context.args)
    if not city:
        await update.message.reply_text("Укажите город. Например: /weather Москва")
        return

    try:
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
    except Exception as e:
        await update.message.reply_text("Не удалось получить данные о погоде.")

handler = CommandHandler("weather", weather)