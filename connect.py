import os
import pyodbc
from common import *


def connect_db():
    con = pyodbc.connect(driver=db_connect['driver'],
                         server=db_connect['server'],
                         database=db_connect['db'],
                         user=db_connect['user'],
                         trusted_connection='yes',
                         password=db_connect['password'],
                         autocommit=True
                         )
    return con
