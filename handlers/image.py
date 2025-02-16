import logging
import requests
import sympy as sp
import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from services.mistral_api import get_mistral_response  # Импорт функции для работы с Mistral API

logger = logging.getLogger(__name__)

async def solve_math_from_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Распознает текст с изображения через OCR.space и решает математические задачи."""
    if not update.message.photo:
        await update.message.reply_text("📸 Отправьте изображение с задачей.")
        return

    try:
        # Скачиваем изображение как бинарные данные
        photo_file = await update.message.photo[-1].get_file()
        image_data = await photo_file.download_as_bytearray()

        # Параметры OCR.space API
        api_key = os.getenv("OCR_SPACE_API_KEY")
        url = "https://api.ocr.space/parse/image"
        headers = {"apikey": api_key}
        
        # Передаем изображение как файл с явным указанием MIME-типа
        files = {"file": ("math_task.jpg", bytes(image_data), "image/jpeg")}
        payload = {
            "language": "rus",  # Только русский язык
            "isOverlayRequired": False,
            "filetype": "JPG",
            "detectOrientation": True
        }

        # Отправляем запрос
        response = requests.post(url, files=files, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Проверка наличия результатов
        if "ParsedResults" not in data or not data["ParsedResults"]:
            error_message = data.get("ErrorMessage", "Неизвестная ошибка OCR")
            logger.error(f"Ошибка OCR: {error_message}")
            await update.message.reply_text(f"❌ Ошибка распознавания: {error_message}")
            return

        # Извлекаем распознанный текст
        parsed_result = data["ParsedResults"][0]
        text = parsed_result.get("ParsedText", "").strip()

        if not text:
            await update.message.reply_text("🔍 Текст не распознан. Убедитесь, что изображение четкое.")
            return

        # Пытаемся решить уравнение с помощью sympy
        try:
            # Убираем лишние символы и пробелы
            equation = text.replace(" ", "").replace(",", ".")
            if "=" not in equation:
                raise ValueError("Уравнение должно содержать знак '='")

            # Разделяем на левую и правую части
            left, right = equation.split("=", 1)
            expr = sp.sympify(f"({left}) - ({right})")
            
            # Решаем уравнение
            x = sp.symbols("x")
            solution = sp.solve(expr, x)
            
            # Форматируем ответ
            response_text = f"✅ *Решение:*\n`x = {solution}`"
            
        except Exception as e:
            logger.error(f"Ошибка решения уравнения: {e}")
            # Если sympy не смог решить, передаем задачу в Mistral API
            try:
                mistral_response = get_mistral_response(
                    f"Реши задачу: {text}. Если это математическая задача, предоставь подробное решение."
                )
                response_text = f"🤖 *Ответ:*\n{mistral_response}"
            except Exception as mistral_error:
                logger.error(f"Ошибка Mistral API: {mistral_error}")
                response_text = (
                    "❌ *Ошибка:* Не удалось решить задачу.\n"
                    "_Убедитесь, что задача записана корректно._"
                )

        await update.message.reply_text(response_text, parse_mode="Markdown")

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса к OCR.space: {str(e)}")
        await update.message.reply_text("🔧 Ошибка соединения с сервисом распознавания.")
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Произошла непредвиденная ошибка. Попробуйте другое изображение.")

# Регистрация обработчика
handler = MessageHandler(filters.PHOTO, solve_math_from_image)