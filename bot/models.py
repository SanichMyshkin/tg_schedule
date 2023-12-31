import sqlite3
import datetime
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'schedule.sql'))


def get_data_of_db(current_data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = f'''SELECT {current_data}.id, LESSON_TIME.time, SUBJECTS.name, TEACHER_NAME.name, CLASSROOMS.name
                FROM {current_data}
                LEFT JOIN LESSON_TIME ON {current_data}.time_id = LESSON_TIME.id
                LEFT JOIN SUBJECTS ON {current_data}.subject_id = SUBJECTS.id
                LEFT JOIN TEACHER_NAME ON {current_data}.teacher_id = TEACHER_NAME.id
                LEFT JOIN CLASSROOMS ON {current_data}.classroom_id = CLASSROOMS.id;'''

    result = cur.execute(query).fetchall()

    cur.close()
    conn.close()
    return result


def get_symbol_of_lesson(number):
    smile_of_day = {
        1: '1️⃣',
        2: '2️⃣',
        3: '3️⃣',
        4: '4️⃣',
        5: '5️⃣',
        6: '6️⃣'
    }
    return smile_of_day[number]


def parse_data(data):
    result = []
    for lesson in data:
        if None in lesson:
            continue
        result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{lesson[2]}"
                      f"\n{lesson[3]}\n{lesson[4]}\n\n")
    return "".join(result)


def week_parse(data, evenness):
    result = [f'Расписание на {evenness} неделю\n\n']
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    count = 0
    for week in data:
        result.append(f'{days_of_week[count]}\n')
        if not week:
            result.append('Выходной\n\n')
        for lesson in week:
            if None in lesson:
                continue
            result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{lesson[2]}"
                          f"\n{lesson[3]}\n{lesson[4]}\n\n")
        count += 1
    return "".join(result)


def get_day_of_week_and_evennes():
    week = int(datetime.datetime.utcnow().isocalendar()[1])
    if week % 2 == 0:
        evennes_of_the_week = 'EVEN'
    else:
        evennes_of_the_week = "ODD"
    day_of_the_week = datetime.datetime.today().weekday() + 1

    return day_of_the_week, evennes_of_the_week


def get_lesson_day(current_data):  # должны передавать день недели
    current_day = current_data[0]
    evennes_week = current_data[1]
    week_days = {
        1: "MONDAY",
        2: "TUESDAY",
        3: "WEDNESDAY",
        4: "THURSDAY",
        5: "FRIDAY",
    }
    return f"{week_days[current_day]}_{evennes_week}"


def tomorrow_day_of_week():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    tomorrow_day = days_of_week[tomorrow.weekday()]
    return f'Расписание на Завтра - {tomorrow_day}, {tomorrow.strftime("%d.%m.%Y")}\n\n'


def today_day_of_week():
    today = datetime.datetime.now()
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    today_day = days_of_week[today.weekday()]
    return f'Расписание на Сегодня - {today_day}, {today.strftime("%d.%m.%Y")}\n\n'


def sunday_switch(current_date):
    if current_date[1] == "ODD":
        return 1, "EVEN"
    else:
        return 1, "ODD"


def next_day(current_data):
    return current_data[0] + 1, current_data[1]
