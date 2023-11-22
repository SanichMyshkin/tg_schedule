from bot.models import get_data_of_db
import json

day = "MONDAY_ODD"

with open('../tests/fixture/database.json', 'r', encoding='utf-8') as f:
    text = json.load(f)
    text = text['TUESDAY_ODD']


def to_set(data):
    result = []
    for element in data:
        result.append(list(element))
    return result


data = to_set(get_data_of_db("MONDAY_ODD"))
print(data)
