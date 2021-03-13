# Все пункты сделать как отдельные функции(можно создавать дополнительные вспомагательные функции)

# 1. Написать функцию, которая принимает в виде параметра целое число - количество цитат (см. урок 12).
# Надо получить ровно столько не повторяющихся цитат с данными и сохранить их в csv файл
# (имя файла сделать параметром по умолчанию).
# Заголовки файла:
# Author, Quote, URL. Если автор не указан, цитату не брать.
# Перед сохранением в csv, записи отсортировать по автору (в алфавитном порядке).

# requests

import json
import time as t
import re
import requests
import csv

url = 'http://api.forismatic.com/api/1.0/'
filename = 'result_csv.csv'


def write_csv(data):
    with open(filename, 'w', encoding="utf-8") as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # не знаю как правильно написать заголовки
        writer.writerows(data)  # не знаю как убрать ненужные ключи


def get_quote(amount):

    data = []
    for num in range(amount):

        params = {'method': 'getQuote',
                  'format': 'json',
                  'key': num,
                  'lang': 'ru'}

        response = requests.get(url, params=params)
        res = response.json()

        while not res['quoteAuthor']:
            response = requests.get(url, params=params)
            res = response.json()

        # print(f"\n{num + 1}. {res['quoteText']}\n   {res['quoteAuthor']}\n   {res['quoteLink']}")

        data.append(res)
        # for key in res:
        #     data[key] = res[key]
    return sorted(data, key=lambda x: x['quoteAuthor'])


write_csv(get_quote(3))

###

# 2. Дан файл authors.txt
# 2.1) написать функцию, которая считывает данные из этого файла,
# возвращая СПИСОК тех строк в которых есть полная дата, писатель и указание на его день рождения или смерти.
# Например: 26th February 1802 - Victor Hugo's birthday - author of Les Misérables.

# 2.2) Написать функцию, которая принимает список строк полученной в пункте 2.1, и возвращает список словарей
# в формате {"name": name, "date": date},
# где name это имя автора, а date - дата из строки в формате "dd/mm/yyyy" (d-день, m-месяц, y-год)

# Например [{"name": "Charles Dickens", "date": "09/06/1870"}, ...,
# {"name": "J. D. Salinger", "date": "01/01/1919"}]

# 2.3) Написать функцию, которая сохраняет результат пункта 2.2 в json файл.

# 2.1)

file_name = 'authors.txt'
look_for_date = r"\d+\w{2}\s\w+\s\d{4}"


def read_txt(file: str) -> list:
    res, data = [], []
    with open(file, 'r') as txt_file:
        data = txt_file.readlines()
        for line in data:
            # if re.findall(look_for_date, line):
            #     res.append(line)
            if 'birthday' in line or 'death' in line:
                res.append(line)
    return res


tmp = read_txt(file_name)
print("Result:" + '\n' + str(tmp))

# 2.2)

look_for_names = r"[A-Z][a-z]+\s[A-Z][a-z]+'"


def create_dict(data: list) -> list:
    result = []
    rep = ['nd', 'th', 'st', 'rd']

    for line in data:
        date = re.findall(look_for_date, line)
        name = line.split("-", 1)[-1]
        name = name.split("'")[0]

        if len(name.split()) <= 3:
            date = ' '.join(date)
            for i in rep:
                date = date.replace(i, '')
            date = t.strptime(date, "%d %B %Y")
            date = t.strftime('%d/%m/%Y', date)
            res = {'name': name, 'date': date}
            result.append(res)
    return result


print('\n' + 'Second result:' + '\n' + str(create_dict(tmp)))

# 2.3)


def write_json(data: list):
    with open('result.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


write_json(create_dict(tmp))