import datetime
import json
import telebot
import schedule
import time
from dotenv import load_dotenv
import os
import sqlite3

nums = int(datetime.datetime.utcnow().isocalendar()[1])
x = datetime.datetime.now()

if (nums % 2) == 0:
    week = 'even_week'

if (nums % 2) != 0:
    week = 'odd_week'

num_week = str(datetime.datetime.today().weekday())

with open('/Users/sanichmyskin/Desktop/bot/database/db.json',
          'r') as json_file:  # тут на ебать через библиотеку os ПРАВОСЛАВНЫЙ путь
    data = json.load(json_file)
    day = data[week][num_week]
    text = []
    for i in day:
        text.append(f'{day[i]["number"]}, {day[i]["subject"]}, {day[i]["cabinet"]}, {day[i]["teacher_name"]}\n')
    messages = ''.join(text)

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('schedule.sql')
cur = conn.cursor()
# cur.execute('CREATE TABLE Week (id INT, Name VARCHAR(255))')
'''var = [
    'ст.пр.Рыбакова А.О.',
    'доц.Адамцевич Л.А.',
    'пр.Воробьев П.Ю.',
    'пр.Жаркая В.Ю.',
    'доц.Федосеева Т.А.',
    'проф.Мезенцев С.Д.',
    'доц.Китайцева Е.Х.',
    'доц.Дуничкин И.В.',
    'доц.Мудрак С.А.',
    'пр.Евстратов В.С.',
    'доц.Куликов В.Г',
    'доц.Князева Н.В.',
    'доц.Демидов Г.В.'

]'''

var = [
    'л.Системотехника строительства',
    'л.Информационное обеспечение систем автоматизации проектирования',
    'л.Автоматизация проектирования инженерных систем и сетей',
    'л.Автоматизация проектирования строительных конструкций',
    'л.Автоматизированные технологии управления проектами',
    'л.Философия',
    'л.Web-технологии в информационных системах',
    'л.Социальный инжиниринг',

    'КОП Информационное обеспечение систем автоматизации проектирования',
    'КОП Автоматизация проектирования инженерных систем и сетей',
    'КОП Автоматизация проектирования строительных конструкций',
    'КОП Web-технологии в информационных системах',

    'пр.Системотехника строительства',
    'пр.Автоматизированные технологии управления проектами',
    'пр.Автоматизация проектирования строительных конструкций',
    'пр.Социальный инжиниринг',

    'КРП Автоматизация проектирования инженерных систем и сетей',
    'КРП Информационное обеспечение систем автоматизации проектирования',
]

x = cur.execute('''SELECT MONDAY_ODD.id, LESSON_TIME.time, SUBJECTS.name, TEACHER_NAME.name, CLASSROOMS.name
FROM MONDAY_ODD
LEFT JOIN LESSON_TIME ON MONDAY_ODD.time_id = LESSON_TIME.id
LEFT JOIN SUBJECTS ON MONDAY_ODD.subject_id = SUBJECTS.id
LEFT JOIN TEACHER_NAME ON MONDAY_ODD.teacher_id = TEACHER_NAME.id
LEFT JOIN CLASSROOMS ON MONDAY_ODD.classroom_id = CLASSROOMS.id;''')
print(list(x))
conn.commit()

# распечатать
'''
SELECT MONDAY_ODD.id, LESSON_TIME.time, SUBJECTS.name, TEACHER_NAME.name, CLASSROOMS.name
FROM MONDAY_ODD
LEFT JOIN LESSON_TIME ON MONDAY_ODD.time_id = LESSON_TIME.id
LEFT JOIN SUBJECTS ON MONDAY_ODD.subject_id = SUBJECTS.id
LEFT JOIN TEACHER_NAME ON MONDAY_ODD.teacher_id = TEACHER_NAME.id
LEFT JOIN CLASSROOMS ON MONDAY_ODD.classroom_id = CLASSROOMS.id;

'''

# создание связи
'''
INSERT INTO "MONDAY_ODD" ("time_id", "subject_id", "teacher_id",  "classroom_id") VALUES (1,  9, 1, 2);
'''
