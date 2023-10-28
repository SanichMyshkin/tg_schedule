import telebot
import schedule
import time
from dotenv import load_dotenv
import os

from models import parse_data, get_data_of_db, get_lesson_day, \
    get_day_of_week_and_evennes, sunday_switch

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)


def send_daily_message():
    current_data = get_day_of_week_and_evennes()
    if current_data[0] == 7:
        current_data = sunday_switch(current_data)
    if int(current_data[0]) >= 5:
        return

    data = get_data_of_db(get_lesson_day(current_data))
    message = parse_data(data)
    if message == '':
        bot.send_message(CHAT_ID, "Поздравляю завтра выходной!")
    else:
        bot.send_message(CHAT_ID, message)


schedule.every().day.at("20:00").do(send_daily_message)

while True:
    schedule.run_pending()
    time.sleep(1)
