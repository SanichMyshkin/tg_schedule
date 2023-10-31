import telebot
from dotenv import load_dotenv
import os
from datetime import datetime
import schedule
import time
from threading import Thread

from models import parse_data, get_data_of_db, get_lesson_day, \
    get_day_of_week_and_evennes, sunday_switch, next_day, tomorrow_day_of_week, today_day_of_week, week_parse

load_dotenv()
CHAT_ID = os.getenv('CHAT_ID')
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['today'])
def main_today(message):
    current_data = get_day_of_week_and_evennes()
    if current_data[0] > 5 or current_data == (2, "ODD"):
        bot.send_message(message.chat.id, f'{today_day_of_week()}'
                                          f'Ничего нет - Отдыхай, башмак\n https://www.youtube.com/shorts/qapArbXRJhk',
                         disable_notification=True)
        return
    data = get_data_of_db(get_lesson_day(current_data))
    messages = parse_data(data)
    bot.send_message(message.chat.id, f'{today_day_of_week()}{messages}', disable_notification=True)


@bot.message_handler(commands=['tomora'])
def main_tomora(message):
    current_data = get_day_of_week_and_evennes()
    tomorrow = next_day(current_data)
    if tomorrow[0] == 8:
        tomorrow = sunday_switch(tomorrow)
    if tomorrow[0] > 5 or tomorrow == (2, "ODD"):
        bot.send_message(message.chat.id, f'{tomorrow_day_of_week()}'
                                          f'Ничего нет - Отдыхай, башмак\n https://www.youtube.com/shorts/qapArbXRJhk',
                         disable_notification=True)
        return
    data = get_data_of_db(get_lesson_day(tomorrow))
    messages = parse_data(data)
    bot.send_message(message.chat.id, f'{tomorrow_day_of_week()}{messages}', disable_notification=True)


@bot.message_handler(commands=['help', 'start'])
def help(message):
    bot.send_message(message.chat.id, "Бот выдает расписание группы ИЦТМС 4-2\n\t"
                                      "/help - выдает инфо о боте\n\t"
                                      "/today - Выдает расписание на сегодня\n\t"
                                      "/tomora - Выдает расписание на завтра\n\t"
                                      "/ODD - Выдает расписание на нечетную неделю\n\t"
                                      "/EVEN - Выдает расписание на четную неделю\n\t")


@bot.message_handler(commands=['ODD', 'EVEN'])
def week(message):
    result = []
    translate = {
        'ODD': 'Нечётную',
        "EVEN": "Чётную"
    }
    for i in range(1, 6):
        cur = get_lesson_day((i, message.text[1:]))
        result.append(get_data_of_db(cur))
    bot.send_message(message.chat.id, week_parse(result, translate[message.text[1:]]), disable_notification=True)


def schedule_time_send():
    schedule.every().day.at("17:00").do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_message():
    current_data = get_day_of_week_and_evennes()
    tomorrow = next_day(current_data)
    if tomorrow[0] == 8:
        tomorrow = sunday_switch(tomorrow)
    if tomorrow[0] > 5 or tomorrow == (2, "ODD"):
        return
    data = get_data_of_db(get_lesson_day(tomorrow))
    messages = parse_data(data)
    bot.send_message(chat_id=CHAT_ID, text=f'{tomorrow_day_of_week()}{messages}', disable_notification=True)


@bot.message_handler(commands=['id'])
def week(message):
    bot.send_message(message.chat.id, message.chat.id)


Thread(target=schedule_time_send).start()
bot.polling(none_stop=True, interval=0)
