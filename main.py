import os
from dotenv import load_dotenv
from telegram.ext import Application
from handlers import start, chat, weather, voice, admin
from utils.logging import setup_logging

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
setup_logging()

# Основная функция
def main() -> None:
    # Создание приложения
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    # Регистрация обработчиков
    application.add_handler(start.handler)
    application.add_handler(chat.handler)
    application.add_handler(weather.handler)
    application.add_handler(voice.handler)
    application.add_handler(admin.handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()