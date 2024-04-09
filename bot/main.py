import telebot
from dotenv import load_dotenv
import os
import schedule
import time
from threading import Thread
from models import parse_data, get_data_of_db, get_lesson_day, \
    get_day_of_week_and_evennes, sunday_switch, next_day, \
    tomorrow_day_of_week, today_day_of_week, week_parse
from weather import get_weather

load_dotenv()
CHAT_ID = os.getenv('CHAT_ID')
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


def send_schedule(chat_id, day, message):
    bot.send_message(chat_id, f'{day}{message}', disable_notification=True)


def get_and_send_schedule(bot, chat_id, day_offset=0):
    current_data = get_day_of_week_and_evennes()
    print(current_data)
    if day_offset != 0:
        current_data = next_day(current_data)
        if current_data[0] >= 7:
            current_data = sunday_switch(current_data)
    if current_data[0] > 5:
        bot.send_message(chat_id, 'Выходной жабы', disable_notification=True)
        return
    data = get_data_of_db(get_lesson_day(current_data))
    messages = parse_data(data)
    if not messages:
        bot.send_message(chat_id, 'Выходной жабы', disable_notification=True)
        return
    day = today_day_of_week() if day_offset == 0 else tomorrow_day_of_week()
    weather = get_weather(
        "today") if day_offset == 0 else get_weather("tomorrow")
    send_schedule(chat_id, day, f'{messages}{weather}')


@bot.message_handler(commands=['today'])
def main_today(message):
    get_and_send_schedule(bot, message.chat.id)


@bot.message_handler(commands=['tomora'])
def main_tomorrow(message):
    get_and_send_schedule(bot, message.chat.id, 1)


@bot.message_handler(commands=['help', 'start'])
def help(message):
    bot.send_message(message.chat.id, "Бот выдает погоду и расписание группы ИЦТМС 4-2\n\t"
                     "/help - выдает инфо о боте\n\t"
                     "/today - Выдает расписание на сегодня\n\t"
                     "/tomora - Выдает расписание на завтра\n\t"
                     "/ODD - Выдает расписание на нечетную неделю\n\t"
                     "/EVEN - Выдает расписание на четную неделю\n\t")


@bot.message_handler(commands=['ODD', 'EVEN'])
def week(message):
    result = []
    translate = {"ODD": 'нечётную', "EVEN": "чётную"}
    for i in range(1, 6):
        cur = get_lesson_day((i, message.text[1:]))
        result.append(get_data_of_db(cur))
    bot.send_message(message.chat.id, week_parse(
        result, translate[message.text[1:]]), disable_notification=True)


def schedule_time_send():
    schedule.every().day.at("08:20").do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_message():
    get_and_send_schedule(bot, CHAT_ID)


@bot.message_handler(commands=['id'])
def get_chat_id(message):
    bot.send_message(message.chat.id, message.chat.id)


Thread(target=schedule_time_send).start()
bot.infinity_polling()
