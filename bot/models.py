import sqlite3
import datetime
import os

db_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'database.sql'))


def get_data_of_db(current_data):
    with sqlite3.connect(db_path) as conn:
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
    return result


def get_symbol_of_lesson(number):
    smile_of_day = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣'}
    return smile_of_day.get(number, '')


def parse_data(data):
    result = []
    for lesson in data:
        if lesson[1] is not None and study_week_wen(lesson[3]):
            result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{
                          lesson[2]}\n{lesson[4]}\n{lesson[5]}\n\n")
    return ''.join(result)


def week_parse(data, evenness):
    result = [f'Расписание на {evenness} неделю\n\n']
    days_of_week = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for count, week in enumerate(data):
        result.append(f'{days_of_week[count]}\n======================\n')
        if not week:
            result.append('Выходной\n\n')
        for lesson in week:
            if lesson[1] is None:
                continue
            if lesson[3]:
                result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{
                              lesson[2]}\n{lesson[3]}\n{lesson[4]}\n{lesson[5]}\n\n")
            else:
                result.append(f"{get_symbol_of_lesson(lesson[0])} {lesson[1]}\n{
                              lesson[2]}\n{lesson[4]}\n{lesson[5]}\n\n")
    return ''.join(result)


def get_day_of_week_and_evennes():
    start_date = datetime.datetime(2024, 1, 1)
    delta = datetime.datetime.now() - start_date
    week = delta.days // 7
    return datetime.datetime.today().weekday() + 1, 'EVEN' if week % 2 == 0 else 'ODD'


def get_lesson_day(current_data):
    week_days = {1: "MONDAY", 2: "TUESDAY",
                 3: "WEDNESDAY", 4: "THURSDAY", 5: "FRIDAY"}
    return f"{week_days.get(current_data[0], '')}_{current_data[1]}"


def tomorrow_day_of_week():
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    days_of_week = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return f'Расписание на Завтра - {days_of_week[tomorrow.weekday()]}, {tomorrow.strftime("%d.%m.%Y")}\n\n'


def today_day_of_week():
    today = datetime.datetime.today()
    days_of_week = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return f'Расписание на Сегодня - {days_of_week[today.weekday()]}, {today.strftime("%d.%m.%Y")}\n\n'


def sunday_switch(current_date):
    return 1, 'EVEN' if current_date[1] == 'ODD' else 'ODD'


def next_day(current_data):
    return current_data[0] + 1, current_data[1]


def count_weeks():
    start_date = datetime.datetime(2024, 2, 12)
    current_date = datetime.datetime.today()
    return (current_date - start_date).days // 7 + 2


def study_week_wen(study_week):
    if study_week:
        study_week = study_week.split(" ")[0]
        numbers_week = [int(num) for num in study_week.split(",")]
        return count_weeks() in numbers_week
    return True
