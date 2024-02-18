import sqlite3
import datetime
import os

db_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'database.sql'))


def get_data_of_db(current_data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = f'''
    SELECT {current_data}.id,
        Lession_time.time,
        Disciplines.name,
        Notes.name,
        Professors.name,
        Rooms.name
        FROM {current_data}
        LEFT JOIN Lession_time ON {current_data}.time_id = Lession_time.id
        LEFT JOIN Disciplines ON {current_data}.discipline_id = Disciplines.id
        LEFT JOIN Notes ON {current_data}.note_id = Notes.id
        LEFT JOIN Professors ON {current_data}.professor_id = Professors.id
        LEFT JOIN Rooms ON {current_data}.room_id = Rooms.id;'''

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
        if lesson[1] is None:
            continue
        if study_week_wen(lesson[3]) == 1 or study_week_wen(lesson[3]):
            result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{lesson[2]}"  # noqa E501
                          f"\n{lesson[4]}\n{lesson[5]}\n\n")
    return "".join(result)


def week_parse(data, evenness):
    result = [f'Расписание на {evenness} неделю\n\n']
    days_of_week = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    count = 0
    for week in data:
        result.append(f'{days_of_week[count]}\n======================\n')
        if not week:
            result.append('Выходной\n\n')
        for lesson in week:
            if lesson[1] is None:
                continue
            if lesson[3] is None:
                result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{lesson[2]}"  # noqa E501
                              f"\n{lesson[4]}\n{lesson[5]}\n\n")
            else:
                result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{lesson[2]}"  # noqa E501
                              f"\nтолько {lesson[3]} (текущая {count_weeks()})"
                              f"\n{lesson[4]}\n{lesson[5]}\n\n")
        count += 1
    return "".join(result)


def get_day_of_week_and_evennes():
    week = int(datetime.datetime.utcnow().isocalendar()[1])
    if week % 2 == 0:
        evennes_of_the_week = 'ODD'
    else:
        evennes_of_the_week = "EVEN"
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
    days_of_week = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    tomorrow_day = days_of_week[tomorrow.weekday()]
    return f'Расписание на Завтра - {tomorrow_day}, {tomorrow.strftime("%d.%m.%Y")}\n\n'  # noqa E501


def today_day_of_week():
    today = datetime.datetime.now()
    days_of_week = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    today_day = days_of_week[today.weekday()]
    return f'Расписание на Сегодня - {today_day}, {today.strftime("%d.%m.%Y")}\n\n'  # noqa E501


def sunday_switch(current_date):
    if current_date[1] == "ODD":
        return 1, "EVEN"
    else:
        return 1, "ODD"


def next_day(current_data):
    return current_data[0] + 1, current_data[1]


def count_weeks():
    start_date = '2024-02-12'  # первая неделя
    current_date = str(datetime.datetime.today().date())
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    delta = current_date - start_date
    weeks = delta.days // 7
    return weeks + 2


def study_week_wen(study_week):
    if study_week:
        study_week = study_week.split(" ")[0]
        numbers_week = [int(num) for num in study_week.split(",")]
        if count_weeks() in numbers_week:
            return True
        return False
    else:
        return 1
