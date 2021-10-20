import numpy
import sqlite3


def getting_values(cells_num=100, table_name='temperature'):
    values = []


    con = sqlite3.connect("data/db/telemetry.sqlite")
    cur = con.cursor()

    values = map(lambda x: x[0], cur.execute(f"""SELECT value FROM {table_name} ORDER BY id DESC LIMIT {cells_num}""").fetchall())
    return list(values)


def