import telebot
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


def send_daily_message():
    chat_id = '-4092622813'
    message = "ТУТ должно быть сообщение с Расписанием на завтра"
    bot.send_message(chat_id, message)


schedule.every().day.at("09:24").do(send_daily_message)

while True:
    schedule.run_pending()
    time.sleep(1)

# тут четность https://www.cyberforum.ru/python-api/thread2631941.html
