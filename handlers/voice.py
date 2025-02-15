import speech_recognition as sr
from telegram import Update
from telegram.ext import MessageHandler, filters

async def voice_handler(update: Update, context) -> None:
    voice_file = await update.message.voice.get_file()
    voice_file.download('voice_message.ogg')

    recognizer = sr.Recognizer()
    with sr.AudioFile('voice_message.ogg') as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            await update.message.reply_text(f"Вы сказали: {text}")
        except sr.UnknownValueError:
            await update.message.reply_text("Не удалось распознать речь.")

handler = MessageHandler(filters.VOICE, voice_handler)