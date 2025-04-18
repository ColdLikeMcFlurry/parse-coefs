import json
import time
import pprint
import pandas as pd
import openpyxl
import pprint as pp
from datetime import datetime, timedelta
from common import sheet_data
from get_season import get_common_lines, expanded_data
from get_top_shelf import expanded_data_to_shelf
from get_train_from_db import trains
from adding import reading_in_thread,reading_season_file, reading_top,reading_days_file


# from adding import add_season, add_day_of_week, add_top_shelf


def define_season_and_day(data):
    # Проходимся по результату expanded_data и находим сезонность и день недели на каждую дату отправления

    res = []
    for sublist in data:
        pre_res = []
        for item in sublist:
            print(item)
            pre_res.append(item)
        pre_res = pd.DataFrame(pre_res)
        pd.set_option('display.max_columns', None)

        try:
            pre_res['Класс обслуживания'] = pre_res['Класс обслуживания'].str.split()
        except Exception as e:
            print(e)

        pre_res = pre_res.explode('Класс обслуживания')
        print(pre_res['Класс обслуживания'])
        min_coef = pre_res['Первый коэффициент'].min()
        pre_res['Сезонность'] = min_coef
        pre_res['День недели'] = pre_res['Первый коэффициент'] / min_coef
        res.append(pre_res)

    res = pd.concat(res).sort_values(by=['Дата', 'Класс обслуживания'])

    res_season = res[['Дата продажи', 'Поезд', 'Дата', 'Класс обслуживания', 'Первый коэффициент', 'Сезонность',
                      'День недели']]

    # print(res_season.to_string())
    # # res_season.to_excel('For base.xlsx', sheet_name='Season')

    return res_season


def define_top_shelf(data):
    # Проходимся по результату expanded_data_to_shelf и собираем  верхнюю полку на каждую дату отправления
    try:
        res = []
        for sublist in data:

            pre_res = []
            for item in sublist:
                # print(item)
                pre_res.append(item)
            pre_res = pd.DataFrame(pre_res)
            try:
                pre_res['Класс обслуживания'] = pre_res['Класс обслуживания'].str.split()
            except Exception as e:
                print(e)
            pre_res = pre_res.explode('Класс обслуживания')
            # min_coef = pre_res['Первый коэффициент'].min()
            # pre_res['Сезонность'] = min_coef
            # pre_res['День недели'] = pre_res['Первый коэффициент'] / min_coef
            # print(pd.DataFrame(pre_res))
            res.append(pre_res)

        res = pd.concat(res).sort_values(by=['Дата', 'Класс обслуживания'])

        res_top_shelf = res[['Дата продажи', 'Поезд', 'Дата', 'Класс обслуживания', 'Первый коэффициент']]
        # print(res_top_shelf.to_string())
        # res.to_excel('For base.xlsx', sheet_name='Top_shelf')

        return res_top_shelf
    except Exception as e:
        print(f'There are 0 coeffs for top_shelf apparently {e}')


def season_and_days(seas):
    today = datetime.today().date()
    date_up = today
    data_seas = []
    data_days = []
    seas['letter_kir'] = seas['Поезд'].apply(lambda x: x[-1] if len(x) == 4 else (x[-2] + x[-1]))
    seas = seas.merge(trains, how='left', left_on='letter_kir', right_on='letter_rus')
    seas['train_en'] = seas['Поезд'].apply(lambda x: x[0:-1] if len(x) == 4 else (x[0:-2])) + seas['letter_lat']
    # проходится по значениями коэффа сезонности
    for i in seas.values:
        # print(i)
        data = {
            'day_of_sale': i[0].date(),
            'train': i[10],
            'dprt_dt': i[2].date(),
            'cabin': i[3],
            'coeff': i[5],
            'date_up': date_up,
            'editor': 'parse-emulator'
        }
        data_seas.append(data)

    # проходится по значениями коэффа дня недели
    for i in seas.values:
        # print(i)
        data = {
            'day_of_sale': i[0].date(),
            'train': i[10],
            'dprt_dt': i[2].date(),
            'cabin': i[3],
            'coeff': i[6],
            'date_up': date_up,
            'editor': 'parse-emulator'
        }
        data_days.append(data)

    # создает json файл с сезонностью
    with open('season.json', 'w', encoding='utf-8') as file_s:
        json.dump(data_seas, file_s, ensure_ascii=False, indent=2, default=str)

    # создает json файл с днем недели
    with open('days.json', 'w', encoding='utf-8') as file_d:
        json.dump(data_days, file_d, ensure_ascii=False, indent=2, default=str)


def tops(top):
    try:
        today = datetime.today().date()
        date_up = today
        data_top=[]
        top['letter_kir'] = top['Поезд'].apply(lambda x: x[-1] if len(x) == 4 else (x[-2] + x[-1]))
        top = top.merge(trains, how='left', left_on='letter_kir', right_on='letter_rus')
        top['train_en'] = top['Поезд'].apply(lambda x: x[0:-1] if len(x) == 4 else (x[0:-2])) + top['letter_lat']

        # проходится по значениями коэффа верхней полки
        for i in top.values:
            # print(i)
            data = {
                'day_of_sale': i[0].date(),
                'train': i[8],
                'dprt_dt': i[2].date(),
                'cabin': i[3],
                'coeff': i[4],
                'date_up': date_up,
                'editor': 'parse-emulator'
            }
            data_top.append(data)
        # создает json файл с верхней полкой
        with open('top.json', 'w', encoding='utf-8') as file_t:
            json.dump(data_top, file_t, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        print(f'Не удалось  создать json файл  {e}')


if __name__ == '__main__':
    # print(sheet_data)
    season = define_season_and_day(expanded_data)
    top_shelf = define_top_shelf(expanded_data_to_shelf)
    season_and_days(season)
    tops(top_shelf)
    reading_in_thread()





    # add_season()
    # add_day_of_week()
    # add_top_shelf()
    # to_excel(season, top_shelf)

# Транспонирование по сезонности
# df_pivot = res.pivot(index=['Дата продажи', 'Поезд', 'Дата'], columns='Класс обслуживания', values='Сезонность')
# df_pivot.reset_index(inplace=True)

# # Замена NaN значений на 1
# df_pivot.fillna(1, inplace=True)
#
# # Просматриваем результат
# print(df_pivot.to_string())


# Функция для генерации коэффициентов на каждый день

# def generate_daily_coefficients(row):
#     # print(row)
#     start_date = row['Начало периода']
#     end_date = row['Конец периода']
#     # Преобразуем дни недели в список
#     days_of_week = []
#     if row['Дни недели'] != 'ВСЕ':
#         for day in str(row['Дни недели']):
#             days_of_week.append(int(day))
#     else:
#         for i in range(1, 8):
#             days_of_week.append(i)
#
#     # print(days_of_week)
#     coefficient = row['Первый коэффициент']
#     # print(coefficient)
#
#     # Генерируем дни в диапазоне и фильтруем по дням недели
#     dates = []
#     current_date = start_date
#     while current_date <= end_date:
#         if current_date.isoweekday() in days_of_week:  # isoweekday: 1 = Понедельник, ..., 7 = Воскресенье
#             # dates.append({'Дата': current_date, 'Коэффициент': coefficient, 'Поезд': row['Поезд'],
#             #               'Класс обслуживания': row['Класс обслуживания']})
#             dates.append({'Дата': current_date, 'Класс обслуживания': row['Класс обслуживания'],
#                           'Первый коэффициент': coefficient})
#
#         current_date += timedelta(days=1)
#     # print(dates)
#     return dates
#
#

# Разворачиваем вложенные списки в единый DataFrame
# result_data = pd.DataFrame([item for sublist in expanded_data for item in sublist])
# min_coef = result_data['Первый коэффициент'].min()
# result_data['Сезонность'] = min_coef
# print(result_data.to_string())
#
#


# # Применяем функцию к каждой строке
# # получаем массив с данными и проходимся по нему
# expanded_data = sheet_data.apply(lambda row: generate_daily_coefficients(row), axis=1)
# # Разворачиваем вложенные списки в единый DataFrame
# result_data = pd.DataFrame([item for sublist in expanded_data for item in sublist])
#
#
# # находим минимальный коэффициент
# min_coef = result_data['Первый коэффициент'].min()
#
# # # Добавим минимальный коэффициент и отношение к нему
# result_data['Сезонность'] = min_coef
# result_data['День недели'] = result_data['Первый коэффициент'] / min_coef
# print(result_data)
# # print(min_coef)
#
# # Транспонирование
# df_pivot = result_data.pivot(index='Дата', columns='Класс обслуживания', values='Сезонность')
# df_pivot.reset_index(inplace=True)
#
# # Замена NaN значений на 1
# df_pivot.fillna(1, inplace=True)
#
# # Просматриваем результат
# # print(df_pivot.to_string())
