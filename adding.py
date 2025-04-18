import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pandas as pd
from connect import connect_db
import os
import json

path = f"{os.path.dirname(os.path.abspath(__file__))}"


# тут код для чтения 3 файлов одновременно
# import json
# from concurrent.futures import ThreadPoolExecutor
#
# def process_season_file():
#     with open(f"{path}/season.json", "r", encoding="utf-8") as file_w:
#         data = json.load(file_w)
#
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         all_records = executor.map(reading_seas, data)
#         for record_group in all_records:
#             add_season_db(record_group)
#
# def process_days_file():
#     with open(f"{path}/days.json", "r", encoding="utf-8") as file_w:
#         data = json.load(file_w)
#
#     with ThreadPoolExecutor(max_workers=30) as executor:
#         all_records = executor.map(reading_days, data)
#         for record_group in all_records:
#             add_days_db(record_group)
#
# def process_top_file():
#     with open(f"{path}/top.json", "r", encoding="utf-8") as file_w:
#         data = json.load(file_w)
#
#     with ThreadPoolExecutor(max_workers=30) as executor:
#         all_records = executor.map(reading_top, data)
#         for record_group in all_records:
#             add_top_db(record_group)
#
# def reading_in_thread():
#     # Запуск трёх потоков одновременно
#     with ThreadPoolExecutor(max_workers=3) as executor:
#         executor.submit(process_season_file)
#         executor.submit(process_days_file)
#         executor.submit(process_top_file)
#
# if name == "__main__":
#     main()


def reading_season_file():
    # Чтение JSON-файла сезонности
    with open(f"{path}/season.json", "r", encoding="utf-8") as file_w:
        data = json.load(file_w)
    # создаем многопоточность для таблицы сезонности
    with ThreadPoolExecutor(max_workers=5) as executor:
        all_records = executor.map(reading_seas, data)
        # Разделение записей
        for record_group in all_records:
            # print(record_group)
            add_season_db(record_group)  # Обработка каждой группы записей


def reading_days_file():
    # Чтение JSON-файла
    with open(f"{path}/days.json", "r", encoding="utf-8") as file_w:
        data = json.load(file_w)
    # создаем многопоточность для таблицы дней недели
    with ThreadPoolExecutor(max_workers=5) as executor:
        all_records = executor.map(reading_days, data)
        # Разделение записей
        for record_group in all_records:
            # print(record_group)
            add_days_db(record_group)  # Обработка каждой группы записей


def read_top_file():
    # Чтение JSON-файла
    with open(f"{path}/top.json", "r", encoding="utf-8") as file_w:
        data = json.load(file_w)
        # создаем многопоточность для таблицы верхней полки
    with ThreadPoolExecutor(max_workers=5) as executor:
        all_records = executor.map(reading_top, data)
        # Разделение записей
        for record_group in all_records:
            # print(record_group)
            add_top_db(record_group)  # Обработка каждой группы записейs


# чтение json файла в несколько потоков
def reading_in_thread():
    # Запуск трёх потоков одновременно
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(reading_season_file)
        executor.submit(reading_days_file)
        executor.submit(read_top_file)


# чтение json файла в несколько потоков
# def reading_in_thread():
#     # Чтение JSON-файла
#     with open(f"{path}/season.json", "r", encoding="utf-8") as file_w:
#         data = json.load(file_w)
#     # создаем многопоточность для таблицы сезонности
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         all_records = executor.map(reading_seas, data)
#         # Разделение записей
#         for record_group in all_records:
#             # print(record_group)
#             add_season_db(record_group)  # Обработка каждой группы записей


def reading_seas(rows):
    # создаем массив для всех значений
    data_season = []
    # print(rows['cabin'])
    data = {
        'day_of_sale': rows['day_of_sale'],
        'train': rows['train'],
        'dprt_dt': rows['dprt_dt'],
        'cabin': '',
        'coeff': rows['coeff'],
        'date_up': rows['date_up'],
        'editor': rows['editor']
    }

    # Тут преобразовываем типы вагонов в обозначения
    # Если два обозначения, то строку приходится дублировать

    if rows.get("cabin") == "ВИП" and rows.get('coeff') > 2.4:
        print('Коэффициент на ВИП > 2.5 в файле season, пропускаем\n')
    # elif rows.get("cabin") == 'NaN':
    #     print('Кабин не была определена\n')
    elif rows.get('cabin') == 'ВИП':
        data['cabin'] = 'F'
        data_season.append(data)
    elif rows.get('cabin') == 'КУПЕ':
        data_1 = data.copy()
        data_1['cabin'] = 'B'
        data_season.append(data_1)
        data_2 = data.copy()
        data_2['cabin'] = 'Y'
        data_season.append(data_2)
    elif rows.get('cabin') == 'СВ':
        data_1 = data.copy()
        data_1['cabin'] = 'C'
        data_season.append(data_1)
        data_2 = data.copy()
        data_2['cabin'] = 'J'
        data_season.append(data_2)
    elif rows.get('cabin') == 'СИД':
        data['cabin'] = 'S'
        data_season.append(data)
    elif rows.get('cabin') == 'СИД-БЗН':
        data['cabin'] = 'D'
        data_season.append(data)
    elif rows['cabin'] == 'ПЛАЦ':
        print('попался плацкарт, пропускаем в файле season\n')
    # print(data_season)
    return data_season


def add_season_db(records):
    for record in records:
        cur = connect_db().cursor()
        train = record['train']  # Маршрут/Поезд
        dprt_dt = record['dprt_dt']  # Дата отправления
        cabin = record['cabin']
        coeff = record['coeff']
        day_of_sale = record['day_of_sale']
        editor = record['editor']
        date_up = record['date_up']
        sql = f"""
                                Select
                                    [day_of_sale],
                                    [train],
                                    [dprt_dt],
                                    [cabin],
                                    [coeff]
                                from [Train].[dbo].[seasons_coeffs]
                                where
                                    day_of_sale = '{day_of_sale}'
                                    and
                                    train = '{train}'
                                    and
                                    dprt_dt = '{dprt_dt}'
                                    and
                                    cabin = '{cabin}'
                                    and
                                    coeff = '{coeff}'
                    """

        cur.execute(sql)
        if cur.fetchone() is None:
            # print(sql)
            print('Данных нет в таблице [seasons_coeffs], записываем')
            # time.sleep(20)
            sql_insert = f"""
                            SET NOCOUNT ON
                    insert into [Train].[dbo].[seasons_coeffs] (day_of_sale,train, dprt_dt, cabin, coeff, date_up, editor)
                        values (
                        '{day_of_sale}',
                        '{train}',
                        '{dprt_dt}',
                        '{cabin}',
                        '{coeff}',
                        '{date_up}',
                        '{editor}')
                    """
            print(sql_insert)
            cur.execute(sql_insert)
            cur.commit()
        else:
            print('Данные имеются в таблице [seasons_coeffs]')
        # cur.commit()


def reading_days(rows):
    # создаем массив для всех значений
    data_days = []

    data = {
        'day_of_sale': rows['day_of_sale'],
        'train': rows['train'],
        'dprt_dt': rows['dprt_dt'],
        'cabin': '',
        'coeff': rows['coeff'],
        'date_up': rows['date_up'],
        'editor': rows['editor']
    }

    # Тут преобразовываем типы вагонов в обозначения
    # Если два обозначения, то строку приходится дублировать

    if rows.get("cabin") == "ВИП" and rows.get('coeff') > 2.4:
        print('Коэффициент на ВИП > 2.5 в файле days, пропускаем \n')
    elif rows.get('cabin') == 'ВИП':
        data['cabin'] = 'F'
        data_days.append(data)
    elif rows.get('cabin') == 'КУПЕ':
        data_1 = data.copy()
        data_1['cabin'] = 'B'
        data_days.append(data_1)
        data_2 = data.copy()
        data_2['cabin'] = 'Y'
        data_days.append(data_2)
    elif rows.get('cabin') == 'СВ':
        data_1 = data.copy()
        data_1['cabin'] = 'C'
        data_days.append(data_1)
        data_2 = data.copy()
        data_2['cabin'] = 'J'
        data_days.append(data_2)
    elif rows.get('cabin') == 'СИД':
        data['cabin'] = 'S'
        data_days.append(data)
    elif rows.get('cabin') == 'СИД-БЗН':
        data['cabin'] = 'D'
        data_days.append(data)
    elif rows['cabin'] == 'ПЛАЦ':
        print('попался плацкарт в файле days, пропускаем\n')

    return data_days


def add_days_db(records):
    for record in records:
        # print(record['train'])

        cur = connect_db().cursor()
        train = record['train']  # Маршрут/Поезд
        dprt_dt = record['dprt_dt']  # Дата отправления
        cabin = record['cabin']
        coeff = record['coeff']
        day_of_sale = record['day_of_sale']
        editor = record['editor']
        date_up = record['date_up']
        sql = f"""
                                Select
                                    [day_of_sale],
                                    [train],
                                    [dprt_dt],
                                    [cabin],
                                    [coeff]
                                from [Train].[dbo].[days_of_the_week]
                                where
                                    day_of_sale = '{day_of_sale}'
                                    and
                                    train = '{train}'
                                    and
                                    dprt_dt = '{dprt_dt}'
                                    and
                                    cabin = '{cabin}'
                                    and
                                    coeff = '{coeff}'
                    """

        cur.execute(sql)
        if cur.fetchone() is None:
            # print(sql)
            print('Данных нет в таблице [days_of_the_week], записываем')
            # time.sleep(20)
            sql_insert = f"""
                            SET NOCOUNT ON
                    insert into [Train].[dbo].[days_of_the_week] (day_of_sale,train, dprt_dt, cabin, coeff, date_up, editor)
                        values (
                        '{day_of_sale}',
                        '{train}',
                        '{dprt_dt}',
                        '{cabin}',
                        '{coeff}',
                        '{date_up}',
                        '{editor}')
                    """
            print(sql_insert)
            cur.execute(sql_insert)
            cur.commit()
        else:
            print('Данные имеются в таблице [days_of_the_week]')


def reading_top(rows):
    # создаем массив для всех значений
    data_top = []

    data = {
        'day_of_sale': rows['day_of_sale'],
        'train': rows['train'],
        'dprt_dt': rows['dprt_dt'],
        'coeff': rows['coeff'],
        'date_up': rows['date_up'],
        'editor': rows['editor']
    }

    # Тут преобразовываем типы вагонов в обозначения
    # Если два обозначения, то строку приходится дублировать

    if rows.get("cabin") == "ВИП" and rows.get('coeff') > 2.4:
        print('Коэффициент на ВИП > 2.5 в файле top, пропускаем\n')
    elif rows['cabin'] == 'ПЛАЦ':
        print('попался плацкарт в файле top, пропускаем\n')

    return data_top


def add_top_db(records):
    for record in records:
        # print(record['train'])

        cur = connect_db().cursor()
        train = record['train']  # Маршрут/Поезд
        dprt_dt = record['dprt_dt']  # Дата отправления
        coeff = record['coeff']
        day_of_sale = record['day_of_sale']
        editor = record['editor']
        date_up = record['date_up']
        sql = f"""
                                Select
                                    [day_of_sale],
                                    [train],
                                    [dprt_dt],
                                    [coeff]
                                from [Train].[dbo].[top_shelf]
                                where
                                    day_of_sale = '{day_of_sale}'
                                    and
                                    train = '{train}'
                                    and
                                    dprt_dt = '{dprt_dt}'
                                    and
                                    coeff = '{coeff}'
                    """

        cur.execute(sql)
        if cur.fetchone() is None:
            # print(sql)
            print('Данных нет в таблице [top_shelf], записываем')
            # time.sleep(20)
            sql_insert = f"""
                            SET NOCOUNT ON
                    insert into [Train].[dbo].[top_shelf] (day_of_sale,train, dprt_dt, cabin, coeff, date_up, editor)
                        values (
                        '{day_of_sale}',
                        '{train}',
                        '{dprt_dt}',
                        '{coeff}',
                        '{date_up}',
                        '{editor}')
                    """
            print(sql_insert)
            cur.execute(sql_insert)
            cur.commit()
        else:
            print('Данные имеются в таблице [top_shelf]')

#
# reading_in_thread()
