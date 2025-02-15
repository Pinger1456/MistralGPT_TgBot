import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_weather(city: str) -> str:
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    )
    response.raise_for_status()
    data = response.json()
    weather_desc = data['weather'][0]['description']
    temp = data['main']['temp']
    return f"Погода в {city}: {weather_desc}, {temp}°C"