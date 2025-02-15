import os
from telegram import Update
from telegram.ext import CommandHandler
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_ID = os.getenv("TELEGRAM_ID")

async def stats(update: Update, context) -> None:
    user_id = update.message.from_user.id
    if user_id != TELEGRAM_ID:
        await update.message.reply_text("У вас нет прав на эту команду.")
        return

    # Логика для сбора статистики
    await update.message.reply_text("Статистика: ...")

handler = CommandHandler("stats", stats)