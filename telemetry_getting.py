import json
from data import db_session
from data.telemetry_class_db import *
import random
import sqlite3
import requests
import asyncio
from config import *


def telemery_dp_main():
    db_session.global_init("data/db/telemetry.sqlite")


def request_to_server():
    resp = requests.get(url=GET_REQ_URL, headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN_RIG}"})
    return resp.text

    """get request"""
    # TODO
    # return '{"_id":"616ebdd44e8df0100016961c","_mid":"616e80369f1bd1001068ac5e","5jr9a":-39,"_oid":"616e833f9f1bd1001068ad11","_ts":1634647508172951,"rz6m8":"84:CC:A8:B0:4B:0C","time":1634647508172,"topic":"rpc_resp","_prsd":1,"nuqg1":"1","gn2oq":true,"meta":{"mac":"84:CC:A8:B0:4B:0C","uid":"1","debug":"1","rssi":"-39","is_ok":"1","uptime":"3962570"},"l03hj":true,"online":true,"sum":null,"payload":"","id":"mqtt-bogdanov_azat_ol-wgdeq4","_gid":"6035e04042ac91001057a7b1","_bot":false,"2tn1i":3962570,"temperature":15.3,"co2":10.1}'

    #with randomizer
    # return '{"_id":"616ebdd44e8df0100016961c","_mid":"616e80369f1bd1001068ac5e","5jr9a":-39,"_oid":"616e833f9f1bd1001068ad11","_ts":1634647508172951,"rz6m8":"84:CC:A8:B0:4B:0C","time":' + str(datetime.datetime.now().timestamp() * 1000) + ',"topic":"rpc_resp","_prsd":1,"nuqg1":"1","gn2oq":true,"meta":{"mac":"84:CC:A8:B0:4B:0C","uid":"1","debug":"1","rssi":"-39","is_ok":"1","uptime":"3962570"},"l03hj":true,"online":true,"sum":null,"payload":"","id":"mqtt-bogdanov_azat_ol-wgdeq4","_gid":"6035e04042ac91001057a7b1","_bot":false,"2tn1i":3962570,"temperature":' + str(random.randint(100, 200) / 10) + ',"co2":' + str(random.randint(100, 200) / 10) + '}'


def data_parsing(raw_data):
    data = json.loads(raw_data)
    print(data)
    add_Temperature(datetime.datetime.fromtimestamp(int(data['state']["time"]) / 1000), data['state']["temperature"])
    add_CO2(datetime.datetime.fromtimestamp(int(data['state']["time"]) / 1000), data['state']["humidity"])


def get_indications_from_db():
    con = sqlite3.connect("data/db/telemetry.sqlite")
    cur = con.cursor()
    try:
        now_temperature_value = str(cur.execute("""SELECT value FROM temperature ORDER BY id DESC LIMIT 1""").fetchall()[0][0])
        now_co2_value = str(cur.execute("""SELECT value FROM co2 ORDER BY id DESC LIMIT 1""").fetchall()[0][0])
        return '{"temperature":' + now_temperature_value + ',"co2":' + now_co2_value + '}'
    except Exception:
        return '{"temperature":"Non","co2":"Non"}'

    # TODO


def cenvert_indications():
    kkk = get_indications_from_db()
    data = json.loads(kkk)
    return '\n'.join(f"{i}\t{str(data[i])}" for i in data)

