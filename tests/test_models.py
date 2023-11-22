import json
import os
from freezegun import freeze_time
from bot.models import get_day_of_week_and_evennes, week_parse, \
    get_lesson_day, sunday_switch, next_day, get_symbol_of_lesson, get_data_of_db, \
    today_day_of_week, tomorrow_day_of_week


class TestTodayAndTomorrow:
    @freeze_time("2024-01-01")
    def test_today_day_of_week(self):
        pass

    @freeze_time("2024-01-01")
    def test_tomorrow_day_of_week(self):
        pass


class TestGetDayOfWeekAndEvenness:
    @freeze_time("2024-01-01")
    def test_data_even(self):
        assert get_day_of_week_and_evennes() == (1, "ODD")

    @freeze_time("2023-11-11")
    def test_data_even_2(self):
        assert get_day_of_week_and_evennes() == (6, "ODD")

    @freeze_time("2024-12-01")
    def test_data_even_3(self):
        assert get_day_of_week_and_evennes() == (7, "EVEN")


class TestGetLessonDay:
    def test_lesson_day(self):
        assert get_lesson_day((1, 'ODD')) == "MONDAY_ODD"
        assert get_lesson_day((2, 'EVEN')) == "TUESDAY_EVEN"
        assert get_lesson_day((5, 'ODD')) == "FRIDAY_ODD"
        assert get_lesson_day((3, 'EVEN')) == "WEDNESDAY_EVEN"


class TestSundaySwitch:
    def test_sunday_switch(self):
        assert sunday_switch((7, 'ODD')) == (1, "EVEN")
        assert sunday_switch((7, "EVEN")) == (1, "ODD")


class TestNextDay:
    def test_next_day(self):
        assert next_day((1, "ODD")) == (2, "ODD")
        assert next_day((2, "ODD")) == (3, "ODD")
        assert next_day((3, "EVEN")) == (4, "EVEN")
        assert next_day((4, "EVEN")) == (5, "EVEN")


class TestGetSymbolOfLesson:
    def test_get_symbol_of_lesson(self):
        assert get_symbol_of_lesson(1) == '1️⃣'
        assert get_symbol_of_lesson(3) == '3️⃣'
        assert get_symbol_of_lesson(6) == '6️⃣'


def to_set(data):
    result = []
    for element in data:
        result.append(list(element))
    return result


class TestGetDataOfDataBase:
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests/fixture/database.json'))

    def test_get_data_of_db(self):
        with open(TestGetDataOfDataBase.file_path, 'r', encoding='utf-8') as file:
            text = json.load(file)
            assert to_set(get_data_of_db('MONDAY_ODD')) == text['MONDAY_ODD']
            assert to_set(get_data_of_db('TUESDAY_EVEN')) == text['TUESDAY_EVEN']
            assert to_set(get_data_of_db('FRIDAY_EVEN')) == text['FRIDAY_EVEN']
            assert to_set(get_data_of_db('THURSDAY_EVEN')) == text['THURSDAY_EVEN']
