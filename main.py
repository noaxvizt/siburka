import logging

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import *
from telemetry_getting import *

"""Bot init"""
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)

"""Logging"""
if DO_LOGS:
    logging.basicConfig(level=logging.INFO)

"""Start func"""


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Состояние датчиков"))
    await message.answer(f"Привет", reply_markup=poll_keyboard)


"""Sensor_consistance func"""


@dp.message_handler(lambda message: message.text == "Состояние датчиков")
async def sensors_consistance(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(f"{cenvert_indications()}", reply_markup=remove_keyboard)


"""getting data prom rigtech"""


async def getting_data_from_server():
    while True:
        await asyncio.sleep(DELAY_TIME)
        data_parsing(request_to_server())


if __name__ == "__main__":

    """db init"""
    telemery_dp_main()
    """async loop"""
    loop = asyncio.get_event_loop()
    loop.create_task(getting_data_from_server())
    loop.create_task(executor.start_polling(dp, skip_updates=True))
    loop.run_forever()
