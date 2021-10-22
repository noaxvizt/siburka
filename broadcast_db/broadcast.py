from main import bot
import asyncio
import sqlite3


def get_users():
    con = sqlite3.connect("broadcast_db/db/broadcast.sqlite")
    cur = con.cursor()
    users = cur.execute(f"""SELECT chat_id FROM users""").fetchall()
    for i in range(len(users)):
        users[i] = users[i][0]
    return users


async def send_message(user_id: int, text: str, disable_notification: bool = False):
    await bot.send_message(user_id, text, disable_notification=disable_notification)


async def broadcaster():
    for user_id in get_users():
        await send_message(user_id, 'жесть')
        await asyncio.sleep(.05)
