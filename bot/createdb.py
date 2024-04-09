import sqlite3

conn = sqlite3.connect('bot/database.sql')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Disciplines
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Lesson_time
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT UNIQUE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Notes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Professors
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Rooms
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)''')

week_days = [
    'MONDAY',
    'TUESDAY',
    'WEDNESDAY',
    'THURSDAY',
    'FRIDAY'
]
evenness_day = ['ODD', 'EVEN']

for day in week_days:
    for evenness in evenness_day:
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS '{day}_{evenness}'
            ('id' INTEGER,
            'time_id' INTEGER,
            'discipline_id' INTEGER,
            'note_id' INTEGER,
            'professor_id' INTEGER,
            'room_id' INTEGER,
                FOREIGN KEY('note_id') REFERENCES 'Notes',
                FOREIGN KEY('discipline_id') REFERENCES 'Disciplines',
                FOREIGN KEY('time_id') REFERENCES 'Lesson_time',
                FOREIGN KEY('room_id') REFERENCES 'Rooms',
                FOREIGN KEY('professor_id') REFERENCES 'Professors',
                PRIMARY KEY('id' AUTOINCREMENT))''')


# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()
