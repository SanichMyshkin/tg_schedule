import telebot
import logging
from dotenv import load_dotenv
import os
import schedule
import time
from threading import Thread
from weather import get_weather

from models import parse_data, get_data_of_db, get_lesson_day, \
    get_day_of_week_and_evennes, sunday_switch, next_day, \
    tomorrow_day_of_week, today_day_of_week, week_parse

load_dotenv()
CHAT_ID = os.getenv('CHAT_ID')
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(filename='bot.log', level=logging.INFO)


@bot.message_handler(commands=['today'])
def main(message):
    try:
        current_data = get_day_of_week_and_evennes()
        if current_data[0] > 5 or current_data == (2, "ODD"):
            bot.send_message(message.chat.id, f'{today_day_of_week()}'
                                              f'{get_weather("today")}'
                                              f'Ничего нет - Отдыхай, башмак\n'
                                              f'https://www.youtube.com/shorts/qapArbXRJhk',
                             disable_notification=True)
            return
        data = get_data_of_db(get_lesson_day(current_data))
        messages = parse_data(data)
        bot.send_message(message.chat.id, f'{today_day_of_week()}{messages}'
                                          f'{get_weather("today")}', disable_notification=True)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка."
                                          "Подробности записаны в логах.", disable_notification=True)


@bot.message_handler(commands=['tomora'])
def main_tomora(message):
    try:
        current_data = get_day_of_week_and_evennes()
        tomorrow = next_day(current_data)
        if tomorrow[0] == 8:
            tomorrow = sunday_switch(tomorrow)
        if tomorrow[0] > 5 or tomorrow == (2, "ODD"):
            bot.send_message(message.chat.id, f'{tomorrow_day_of_week()}'
                                              f'Ничего нет - Отдыхай, башмак\n{get_weather("tomorrow")}'
                                              f'https://www.youtube.com/shorts/qapArbXRJhk',
                             disable_notification=True)
            return
        data = get_data_of_db(get_lesson_day(tomorrow))
        messages = parse_data(data)
        bot.send_message(message.chat.id, f'{tomorrow_day_of_week()}{messages}{get_weather("tomorrow")}',
                         disable_notification=True)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка."
                                          "Подробности записаны в логах.", disable_notification=True)


@bot.message_handler(commands=['help', 'start'])
def help(message):
    try:
        bot.send_message(message.chat.id, "Бот выдает погоду и расписание группы ИЦТМС 4-2\n\t"
                                          "/help - выдает инфо о боте\n\t"
                                          "/today - Выдает расписание на сегодня\n\t"
                                          "/tomora - Выдает расписание на завтра\n\t"
                                          "/ODD - Выдает расписание на нечетную неделю\n\t"
                                          "/EVEN - Выдает расписание на четную неделю\n\t")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка."
                                          "Подробности записаны в логах.", disable_notification=True)


@bot.message_handler(commands=['ODD', 'EVEN'])
def week(message):
    try:
        result = []
        translate = {
            'ODD': 'Нечётную',
            "EVEN": "Чётную"
        }
        for i in range(1, 6):
            cur = get_lesson_day((i, message.text[1:]))
            result.append(get_data_of_db(cur))
        bot.send_message(message.chat.id, week_parse(result, translate[message.text[1:]]), disable_notification=True)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка."
                                          "Подробности записаны в логах.", disable_notification=True)


def schedule_time_send():
    try:
        schedule.every().day.at("05:30").do(send_message)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logging.error(f"An error occurred in schedule_time_send: {str(e)}")


def send_message():
    try:
        current_data = get_day_of_week_and_evennes()
        if current_data[0] > 5 or current_data == (2, "ODD"):
            return
        data = get_data_of_db(get_lesson_day(current_data))
        messages = parse_data(data)
        bot.send_message(chat_id=CHAT_ID, text=f'{today_day_of_week()}{messages}'
                                               f'{get_weather("today")}', disable_notification=True)
    except Exception as e:
        logging.error(f"An error occurred in send_message: {str(e)}")


@bot.message_handler(commands=['id'])
def get_chat_id(message):
    try:
        bot.send_message(message.chat.id, message.chat.id)
    except Exception as e:
        logging.error(f"An error occurred in get_chat_id: {str(e)}")


Thread(target=schedule_time_send).start()
bot.polling(none_stop=True, interval=0)
