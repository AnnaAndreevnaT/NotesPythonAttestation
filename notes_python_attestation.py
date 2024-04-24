
import os
import json
import datetime


INFO_STRING = """ 
Выберите режим работы:
1 - вывести все данные
2 - добавление новой заметки
3 - поиск заметок по дате (формат ДД/ММ/ГГГГ)
4 - редактирование заметки по пометке
5 - выход
6 - удалить заметку
"""


class IndexExistsException(Exception):
    def __init__(self, index):
        self.index = index


    def __str__(self):
        return f"Заметка с пометкой {self.index} существует, выберите другую пометку"
    

class IndexDoesNotExistsException(Exception):
    def __init__(self, index):
        self.index = index


    def __str__(self):
        return f"Заметки с пометкой {self.index} не существует, выберите другую пометку"


DATASOURCE = 'notes.json'


def check_directory(filename: str):
    if filename not in os.listdir():
        with open(filename, 'w', encoding = 'utf-8') as data:
            data.write("{}")


check_directory(DATASOURCE)


def format_output(input: dict):
    result = {k: f"{v['info']}, сделана: {v['date']}" for k, v in input.items()}
    result = [f"Пометка {k}, текст заметки: {result[k]}" for k in result.keys()]
    result = '\n'.join(result)
    return result


def add_new_note(index: str, info:str, filename: str):
    with open(filename, 'r', encoding='utf-8') as rdbl:
       data = json.load(rdbl)
    with open(filename, 'w', encoding='utf-8') as wrtbl:
       if index in data.keys():
           json.dump(data, wrtbl)
           raise IndexExistsException(index)
       data[index] = {
           "date": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
           "info": info
           }
       json.dump(data, wrtbl)


def read_all(filename: str) -> str:
    with open(filename, 'r', encoding = 'utf-8') as wrtbl:
        data = json.load(wrtbl)
        return format_output(data)


def search_note(filename: str, date: str=None) -> tuple:
    with open(filename, 'r', encoding = 'utf-8') as wrtbl:
        data = json.load(wrtbl)
        result = {k: v for k, v in data.items() if v["date"].split(',')[0] == date}
        return format_output(result)      


def edit_note(index: str, info:str, filename: str):
    with open(filename, 'r', encoding='utf-8') as rdbl:
       data = json.load(rdbl)
    with open(filename, 'w', encoding='utf-8') as wrtbl:
       if index not in data.keys():
           json.dump(data, wrtbl)
           raise IndexDoesNotExistsException(index)
       data[index] = {
           "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
           "info": info
           }
       json.dump(data, wrtbl)


def delete_note(index: str, filename: str):
    with open(filename, 'r', encoding='utf-8') as rdbl:
       data = json.load(rdbl)
    with open(filename, 'w', encoding='utf-8') as wrtbl:
       if index not in data.keys():
           json.dump(data, wrtbl)
           raise IndexDoesNotExistsException(index)
       del data[index]
       json.dump(data, wrtbl)


while True:
    try:
        mode = int(input(INFO_STRING))
        if mode == 1:        
            print(read_all(DATASOURCE))
        elif mode == 2:
            index = input("Пометка: ")
            info = input("Заметка: ")
            add_new_note(index=index, info=info, filename=DATASOURCE)
        elif mode == 3:
            date = input("Дата (формат ДД/ММ/ГГГГ): ")
            res = search_note(filename=DATASOURCE, date=date)      
            print(res)
        elif mode == 4:
            index = input("Пометка: ")
            info = input("Заметка: ")
            edit_note(index=index, info=info, filename=DATASOURCE)
        elif mode == 5:
            break
        elif mode == 6:
            index = input("Пометка: ")
            delete_note(index=index, filename=DATASOURCE)

    except Exception as e:
        print(str(e))
        continue

