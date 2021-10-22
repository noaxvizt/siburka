import datetime
import sqlalchemy
import sqlite3
from .db_session import SqlAlchemyBase, create_session, global_init


class Users(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)


def add_user(chat_id):
    now = Users()
    now.chat_id = chat_id
    try:
        db_sess = create_session()
        db_sess.add(now)
        db_sess.commit()
        return f"Позьзователь с id {chat_id} теперь подписан на бота"
    except Exception:
        return f"Пользователь с id {chat_id} был подписан на бота"


def remove_user(chat_id):
    print(chat_id)
    con = sqlite3.connect("broadcast_db/db/broadcast.sqlite")
    cur = con.cursor()
    cur.execute(f"""DELETE FROM users WHERE chat_id = {chat_id}""")
    con.commit()
    return f"Пользователь с id {chat_id} больше не подписан на бота"


def broadcast_dp_main():
    global_init("broadcast_db/db/broadcast.sqlite")


