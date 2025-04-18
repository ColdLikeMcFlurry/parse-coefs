import pandas as pd
import openpyxl
import pprint as pp
from datetime import datetime, timedelta
from common import sheet_data


# функция, которая собирает одинаковые строки вместе, а уникальные строки отдельно
def get_common_lines_top_shelf():
    # Выбор нужных столбцов для сравнения
    columns_to_compare = ['Поезд', 'Класс обслуживания', 'Дата продажи', 'Начало периода', 'Конец периода']

    # Создание словаря для хранения групп строк
    groups = {}

    # Цикл по строкам
    for i in range(len(sheet_data)):
        # print(i)
        # пропускаем строку, если она невалидна
        if not sheet_data.iloc[i]['Валидное']:
            continue
        # пропускаем строку, елсли там  не верхняя полка
        if not sheet_data.iloc[i]['Скидка на верхнюю полку']:
            continue

        current_row = sheet_data.iloc[i]
        # print(data.iloc[i])
        current_values = tuple(current_row[columns_to_compare])
        # print(current_values)

        if current_values in groups:
            groups[current_values].append(i)

        else:
            groups[current_values] = [i]

    grouped_rows = []
    unique_rows = []
    # Разделение строк на группы по одинаковым и уникальным значениям
    for indices in groups.values():
        if len(indices) > 1:
            grouped_rows.append(indices)
        else:
            unique_rows.append(indices[0])

    # print("Группы строк с одинаковыми значениями:")
    # print(grouped_rows)
    #
    # print("Строки с уникальными значениями:")
    # print(unique_rows)

    # собираем данные в общий массив
    all_lines = grouped_rows + unique_rows

    print("Строки всеми значениями для верхней полки:")
    print(all_lines)
    # print(groups)
    return all_lines


# в данной функции мы определяем коэффициент сезонности на дату отправления
def generate_coeffs_top_shelf():
    dates = []
    for i in get_common_lines_top_shelf():
        dates_periods = []

        # тут смотим одиночные строки
        if type(i) is int:
            # определяем начало и конец периода
            start_date = sheet_data.iloc[i]['Начало периода']
            end_date = sheet_data.iloc[i]['Конец периода']

            # создаем массив с числами дней недели
            days_of_week = []
            if sheet_data.iloc[i]['Дни недели'] != 'ВСЕ':
                for day in str(sheet_data.iloc[i]['Дни недели']):
                    days_of_week.append(int(day))
            else:
                for k in range(1, 8):
                    days_of_week.append(k)

            # определяем коэффициент текущей строки
            coefficient = sheet_data.iloc[i]['Первый коэффициент']
            day_of_sale = sheet_data.iloc[i]['Дата продажи']

            # Генерируем дни в диапазоне и фильтруем по дням недели
            current_date = start_date
            while current_date <= end_date:
                if current_date.isoweekday() in days_of_week:  # isoweekday: 1 = Понедельник, ..., 7 = Воскресенье
                    # dates.append({'Дата': current_date, 'Коэффициент': coefficient, 'Поезд': row['Поезд'],
                    #               'Класс обслуживания': row['Класс обслуживания']})
                    dates_periods.append(
                        {'Дата продажи': day_of_sale, 'Дата': current_date,
                         'Класс обслуживания': sheet_data.iloc[i]['Класс обслуживания'],
                         'Поезд': sheet_data.iloc[i]['Поезд'],
                         'Первый коэффициент': coefficient})
                current_date += timedelta(days=1)
            dates.append(dates_periods)
        # тут смотри парные строки
        else:
            for j in i:
                # определяем начало и конец периода
                start_date = sheet_data.iloc[j]['Начало периода']
                end_date = sheet_data.iloc[j]['Конец периода']

                # создаем массив с числами дней недели
                days_of_week = []
                if sheet_data.iloc[j]['Дни недели'] != 'ВСЕ':
                    for day in str(sheet_data.iloc[j]['Дни недели']):
                        days_of_week.append(int(day))
                else:
                    for k in range(1, 8):
                        days_of_week.append(k)
                # print(start_date, end_date)

                # определяем коэффициент текущей строки
                coefficient = sheet_data.iloc[j]['Первый коэффициент']
                day_of_sale = sheet_data.iloc[j]['Дата продажи']
                # print(coefficient)

                # Генерируем дни в диапазоне и фильтруем по дням недели
                # dates = []
                current_date = start_date
                while current_date <= end_date:
                    if current_date.isoweekday() in days_of_week:  # isoweekday: 1 = Понедельник, ..., 7 = Воскресенье
                        # dates.append({'Дата': current_date, 'Коэффициент': coefficient, 'Поезд': row['Поезд'],
                        #               'Класс обслуживания': row['Класс обслуживания']})
                        dates_periods.append(
                            {'Дата продажи': day_of_sale,
                             'Дата': current_date,
                             'Класс обслуживания': sheet_data.iloc[j]['Класс обслуживания'],
                             'Поезд': sheet_data.iloc[j]['Поезд'],
                             'Первый коэффициент': coefficient})
                    current_date += timedelta(days=1)
            dates.append(dates_periods)
        # print(dates_periods)
    # print(dates)
    return dates


expanded_data_to_shelf = generate_coeffs_top_shelf()
# pp.pprint(expanded_data_to_shelf)
# pp.pprint(expanded_data_to_shelf)
