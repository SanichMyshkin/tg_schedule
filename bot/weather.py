from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()
WEATHER_API_TOKEN = os.getenv("WEATHER_API_KEY")


def get_weather(day):
    location = "москва"
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    unix_timestamp = tomorrow.strftime("%s") if day == "tomorrow" else ""

    url = (
        f"http://api.openweathermap.org/data/2.5/forecast?q={location}"
        f"&lang=ru&units=metric&appid={WEATHER_API_TOKEN}&dt={unix_timestamp}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        return "ОШИБКА ПОЛУЧЕНИЯ ПОГОДЫ!"

    weather_data = response.json()
    cur_weather = next(
        (
            data["main"]["temp"]
            for data in weather_data["list"]
            if not unix_timestamp or data["dt"] == int(unix_timestamp)
        ),
        "",
    )
    weather_feels = next(
        (
            data["main"]["feels_like"]
            for data in weather_data["list"]
            if not unix_timestamp or data["dt"] == int(unix_timestamp)
        ),
        "",
    )
    weather_symbol = next(
        (
            data["weather"][0]["main"]
            for data in weather_data["list"]
            if not unix_timestamp or data["dt"] == int(unix_timestamp)
        ),
        "",
    )
    weather_description = next(
        (
            data["weather"][0]["description"].capitalize()
            for data in weather_data["list"]
            if not unix_timestamp or data["dt"] == int(unix_timestamp)
        ),
        "",
    )
    wind = next(
        (
            data["wind"]["speed"]
            for data in weather_data["list"]
            if not unix_timestamp or data["dt"] == int(unix_timestamp)
        ),
        "",
    )

    code_to_smile = {
        "Clear": "☀",
        "Clouds": "☁",
        "Rain": "🌧",
        "Drizzle": "🌦",
        "Snow": "❄",
        "Thunderstorm": "⛈",
    }

    wd = code_to_smile.get(
        weather_symbol, "Посмотри в окно, я не понимаю, что там за погода..."
    )

    return f"Погода в городе: {weather_data['city']['name']}\nТемпература: {cur_weather} °C / Ощущается как {weather_feels} °C\n{weather_description} {wd}\nВетер: {wind} м/с\n"
