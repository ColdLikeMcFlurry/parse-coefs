from connect import connect_db
import pandas as pd


def read(sql):
    try:
        cur = connect_db().cursor()
        conn = connect_db()
        sql = f"""
            {sql}"""
        # print(sql)
        df_sql = pd.read_sql(sql, conn)
        conn.close()
        cur.close()
        # print(df_sql)
        # cur.execute(sql)
        # cur.commit()

        return df_sql
    except Exception as e:
        print(e)


get_trains = f"""SELECT DISTINCT [kir] as letter_rus, [lat] as letter_lat FROM [Train].[dbo].[translit]
 """
trains = read(get_trains)
# print(trains)
# where day_of_sale >= '2023-01-01' and train_rus not LIKE '9%' and train_rus not LIKE '8%' and
# train_rus is not NULL and train is not null


