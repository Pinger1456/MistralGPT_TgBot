from telegram import Update
from telegram.ext import MessageHandler, filters
from services.mistral_api import get_mistral_response

async def chat(update: Update, context) -> None:
    user_message = update.message.text

    try:
        # Добавляем указание языка
        prompt = f"Отвечай на русском, но где необходимо используй другие языки: {user_message}"
        
        # Запрос к API
        bot_response = get_mistral_response(prompt)
    except Exception as e:
        bot_response = "Произошла ошибка при обработке вашего запроса. Попробуйте позже."

    await update.message.reply_text(bot_response)

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chat)