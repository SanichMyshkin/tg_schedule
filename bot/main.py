import telebot
import schedule
import time
from dotenv import load_dotenv
import os

from models import parse_data, get_data_of_db, get_lesson_day, \
    get_day_of_week_and_evennes, sunday_switch, next_day

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)


def send_daily_message():
    current_data = get_day_of_week_and_evennes()
    tomorrow = next_day(current_data)
    if current_data[0] == 7:
        current_data = sunday_switch(tomorrow)
    if int(current_data[0]) >= 5:
        return

    data = get_data_of_db(get_lesson_day(tomorrow))
    message = parse_data(data)
    if tomorrow == (2, "ODD"):
        bot.send_message(CHAT_ID, message + "Пар на завтра нет, отдыхаем!")
    else:
        bot.send_message(CHAT_ID, message)


schedule.every().day.at("20:00").do(send_daily_message)

while True:
    schedule.run_pending()
    time.sleep(1)
