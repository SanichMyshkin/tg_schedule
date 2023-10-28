import telebot
from dotenv import load_dotenv
import os

from models import parse_data, get_data_of_db, get_lesson_day, \
    get_day_of_week_and_evennes, sunday_switch, next_day

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['today'])
def main(message):
    current_data = get_day_of_week_and_evennes()
    if current_data[0] == 7:
        current_data = sunday_switch(current_data)
    if current_data[0] > 5 or current_data == (2, "ODD"):
        bot.send_message(message.chat.id, 'Пар сегодня нет!\nОтдыхай, башмак')
        return
    data = get_data_of_db(get_lesson_day(current_data))
    message = parse_data(data)
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['tomora'])
def main(message):
    current_data = get_day_of_week_and_evennes()
    tomorrow = next_day(current_data)
    if tomorrow[0] == 8:
        tomorrow = sunday_switch(tomorrow)
    if tomorrow[0] > 5 or tomorrow == (2, "ODD"):
        bot.send_message(message.chat.id, 'Пар завтра нет!\nОтдыхай, башмак')
        return
    data = get_data_of_db(get_lesson_day(current_data))
    message = parse_data(data)
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Бот выдает расписание и порицает татар\n\t/help - выдает инфо о боте\n\t"
                                      "/today - Выдает расписание на сегодня\n\t"
                                      "/tomora - Выдает расписание на завтра")


@bot.message_handler(commands=['id'])
def main(message):
    bot.send_message(message.chat.id, message)


bot.polling(none_stop=True)
