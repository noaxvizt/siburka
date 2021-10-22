import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import *
from telemetry_getting import *
from aiogram import types
from broadcast_db.broadcast_class_db import *


"""Bot init"""
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)


"""Logging"""
if DO_LOGS:
    logging.basicConfig(level=logging.INFO)

"""Start func"""


async def set_default_commands():
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить"),
        types.BotCommand("equipments", "Оборудования"),
        types.BotCommand("sub", "Подписку"),
        types.BotCommand("unsub", "Cоздать подписку на обновления"),
        types.BotCommand("temp", "Температура"),
        types.BotCommand("co2", "Углекислого газ")
    ])


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    # poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # poll_keyboard.add(types.KeyboardButton(text="Показания датчика температуры", ))
    # poll_keyboard.add(types.KeyboardButton(text="Показания датчика углекислого газа"))
    await message.answer(f"""
    Добро пожаловать, {message.from_user.username}
    Рады Вас приветствовать в телеграм боте мониторинга оборудования на производстве: 
    ⚙️ Рекомендуем ознакомиться со следующим списком команд:
    /start - главная страница
    /equipments - открыть список оборудований
    /sub - создать подписку на обновления
    /unsub - прекратить подписку на обновления
    ⚙️ Команды для мониторинга оборудования: 
    /temp - Отслеживание уровня температуры
    /co2 - Отслеживание уровня углекислого газа""")


"""Sensor_consistance func"""


@dp.message_handler(commands=['temp'])
async def temp_sensors_condition(message: types.Message):
    await message.answer(f"{cenvert_indications('temperature')} \n Назад /start")


@dp.message_handler(commands=['co2'])
async def temp_sensors_condition(message: types.Message):
    await message.answer(f"{cenvert_indications('co2')} \n Назад /start")


@dp.message_handler(commands=['sub'])
async def temp_sensors_condition(message: types.Message):
    await message.answer(add_user(message.chat.id))


@dp.message_handler(commands=['unsub'])
async def temp_sensors_condition(message: types.Message):
    await message.answer(remove_user(message.chat.id))


@dp.message_handler(commands=['equipments'])
async def our_equipments(message: types.Message):
    await message.answer("На данный момент мы проводим мониторинг с Завода Тесла и измеряем следующие показатели: температура, уровень с02 \n Назад /start")


@dp.message_handler(lambda message: message.text == "График")
async def graph_sensors_consistance(message: types.Message):
    photo = open('files/images/foo.png', 'b')
    await bot.send_photo(message.message_id, photo)
    await message.answer("Ало")


@dp.message_handler(content_types=['text'])
async def temp_sensors_condition(message: types.Message):
    await message.answer(f"Я не понял, что вы имеете ввиду")


async def getting_data_from_server(loop):
    while True:
        await asyncio.sleep(DELAY_TIME)
        data_parsing(request_to_server(loop))


if __name__ == "__main__":

    """db init"""
    telemetry_dp_main()
    broadcast_dp_main()
    """async loop"""
    loop = asyncio.get_event_loop()
    loop.create_task(set_default_commands())
    loop.create_task(getting_data_from_server(loop))
    loop.create_task(executor.start_polling(dp, skip_updates=True))
    loop.run_forever()

