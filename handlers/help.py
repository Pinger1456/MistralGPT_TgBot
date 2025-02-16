from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Текст справки
    help_text = """
    🤖 *Доступные команды:*

    /start - Начать диалог с ботом.
    /help - Показать это сообщение.
    /clear - Очистить историю разговора.
    /weather <город> - Узнать погоду в указанном городе.

    📝 *Как использовать бота:*
    - Просто напишите мне что-нибудь, и я постараюсь вам ответить!
    - Вы также можете отправлять голосовые сообщения.
    """
    
    # Отправляем сообщение с помощью Markdown
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Регистрация обработчика
handler = CommandHandler("help", help_command)