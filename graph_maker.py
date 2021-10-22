import numpy as np
import sqlite3
import datetime
import matplotlib.pyplot as plt
from config import *


def getting_values(table_name, num_of_values=100):
    con = sqlite3.connect("telemetry_db/db/telemetry.sqlite")
    cur = con.cursor()

    values = map(lambda x: x[0], cur.execute(f"""SELECT value FROM {table_name} ORDER BY id DESC LIMIT {num_of_values}""").fetchall())
    return list(values)


def make_graph(num_of_values, table_name='temperature'):
    y = getting_values(table_name, num_of_values)
    x = [datetime.datetime.now() + datetime.timedelta(seconds=i * DELAY_TIME) for i in range(len(y))]
    plt.plot(x, y, label='Реальные значения')
    plt.axhline(y=KRITICAL_PARAMETRS[table_name], color='red', label='Предельнодопустимые значения')
    plt.xlabel('time', color='gray')
    plt.ylabel(table_name, color='gray')
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig('files/images/foo.png')


make_graph(1000)


