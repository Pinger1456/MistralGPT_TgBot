def format_weather_response(data: dict) -> str:
    return f"Погода в {data['name']}: {data['weather'][0]['description']}, {data['main']['temp']}°C"