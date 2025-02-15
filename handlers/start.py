from telegram import Update
from telegram.ext import CommandHandler

async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Я бот с интеграцией Mistral AI. Напиши мне что-нибудь.')

handler = CommandHandler("start", start)