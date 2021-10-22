import json
from telemetry_db import db_session
from telemetry_db.telemetry_class_db import *
import sqlite3
import requests
from config import *
from broadcast_db.broadcast import broadcaster


def telemetry_dp_main():
    db_session.global_init("telemetry_db/db/telemetry.sqlite")


def request_to_server(loop):
    resp = requests.get(url=GET_REQ_URL, headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN_RIGTECH}"})
    return resp.text, loop


def data_parsing(raw_data):
    data = json.loads(raw_data[0])
    if data['state']["temperature"] >= KRITICAL_PARAMETRS['temperature']:
        raw_data[1].create_task(broadcaster())
    add_Temperature(datetime.datetime.fromtimestamp(int(data['state']["time"]) / 1000), data['state']["temperature"])
    add_CO2(datetime.datetime.fromtimestamp(int(data['state']["time"]) / 1000), data['state']["humidity"])


def get_temp_indications_from_db():
    con = sqlite3.connect("telemetry_db/db/telemetry.sqlite")
    cur = con.cursor()
    try:
        now_temperature_value = str(cur.execute("""SELECT value FROM temperature ORDER BY id DESC LIMIT 1""").fetchall()[0][0])
        return '{"Температура":' + now_temperature_value + '}'
    except Exception:
        return '{"Температура":"Non"}'


def get_co2_indications_from_db():
    con = sqlite3.connect("telemetry_db/db/telemetry.sqlite")
    cur = con.cursor()
    try:
        now_co2_value = str(cur.execute("""SELECT value FROM co2 ORDER BY id DESC LIMIT 1""").fetchall()[0][0])
        return '{"Уровень co2":' + now_co2_value + '}'
    except Exception:
        return '{"Уровень co2":"Non"}'


def cenvert_indications(sensor_name):
    if sensor_name == 'temperature':
        raw_data = get_temp_indications_from_db()
    else:
        raw_data = get_co2_indications_from_db()
    # else:
    #     raw_data = get_indications_from_db()
    data = json.loads(raw_data)
    return '\n'.join(f"{i}\t{str(data[i])}" for i in data)

