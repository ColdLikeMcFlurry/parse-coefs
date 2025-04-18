import pandas as pd
import openpyxl
import pprint as pp
from datetime import datetime, timedelta

# читаем файл
# sheet_data = pd.read_excel('C:\GitRepository\parse_coefs\Чекер.xlsx')
a = fr'C:/Users/MaslovAP/PycharmProjects/parse-coefficients-txt-terminal/Чекер.xlsx'
sheet_data = pd.read_excel(a)
# определяем нужные столбцы
columns = ['Поезд', 'Нитки', 'Класс обслуживания', 'Скидка на верхнюю полку', 'Дни недели', 'Перевозчик',
           'Дата продажи', 'Начало периода', 'Конец периода', 'Первый коэффициент', 'Второй коэффициент', 'Различаются',
           'Валидное']

sheet_data = sheet_data[columns]

# print(sheet_data)

# Преобразуем даты в формате строк в datetime для удобной обработки
sheet_data['Начало периода'] = pd.to_datetime(sheet_data['Начало периода'], format='%d.%m.%y')
sheet_data['Конец периода'] = pd.to_datetime(sheet_data['Конец периода'], format='%d.%m.%y')
sheet_data['Дата продажи'] = pd.to_datetime(sheet_data['Дата продажи'], format='%d.%m.%y')

# Константы для подключения к БД
SQL_driver = '{ODBC Driver 17 for SQL Server}'
SQL_server = 'FPC-KONKUR-AS1'
SQL_DB = 'Train'
SQL_user = 'FPC\ZhigachevDA'
SQL_password = 'zD@741852963'


ip = {
    'mssql': 'FPC-KONKUR-AS1',
}

mssql = {
    'host': ip['mssql'],
    'password': '^^Fhf[ybls46',
    'user': 'FPC\MadyshevAV',
    'db': 'Train',
    'port': 1433,
    'cnct': 'mssql+pymssql'
}

db_connect = {
    'driver': "{ODBC Driver 17 for SQL Server}",
    'server': 'FPC-KONKUR-AS1',
    'db': 'Train',
    'user': 'FPC\ZhigachevDA',
    'password': 'zD@741852963'
}
