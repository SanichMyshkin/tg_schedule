from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()
WEATHER_API_TOKEN = os.getenv('WEATHER_API_KEY')


def get_weather(day):
    location = 'москва'
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if day == "tomorrow":
        unix_timestamp = tomorrow.strftime('%s')
    else:
        unix_timestamp = ''

    url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}' \
          f'&lang=ru&units=metric&appid={WEATHER_API_TOKEN}&dt={unix_timestamp}'

    response = requests.get(url)
    if response.status_code != 200:
        return 'ОШИБКА ПОЛУЧЕНИЯ ПОГОДЫ!'

    weather_data = response.json()
    city = weather_data['city']['name']
    cur_weather = ''
    weather_feels = ''
    weather_symbol = ''
    weather_description = ''
    wind = ""
    for data in weather_data['list']:
        if not unix_timestamp or data['dt'] == int(unix_timestamp):
            cur_weather = data['main']['temp']
            weather_feels = data['main']['feels_like']
            weather_symbol = data['weather'][0]['main']
            weather_description = data['weather'][0]['description']
            wind = data['wind']['speed']
            break

    code_to_smile = {
        "Clear": "☀",
        "Clouds": "☁",
        "Rain": "🌧",
        "Drizzle": "🌦",
        "Snow": "❄",
        "Thunderstorm": "⛈",
    }

    if weather_symbol in code_to_smile:
        wd = code_to_smile[weather_symbol]
    else:
        wd = "Посмотри в окно, я не понимаю, что там за погода..."

    return f"Погода в городе: {city}\nТемпература: {cur_weather} °C / Ощущается как {weather_feels}°C" \
           f"\n{weather_description.capitalize()} {wd}\nВетер: {wind} м/с \n"
