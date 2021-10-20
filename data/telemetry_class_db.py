import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, create_session


class Temperature_db(SqlAlchemyBase):
    __tablename__ = 'temperature'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sent_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    value = sqlalchemy.Column(sqlalchemy.Float)


class CO2_db(SqlAlchemyBase):
    __tablename__ = 'co2'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sent_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    value = sqlalchemy.Column(sqlalchemy.Float)


def add_Temperature(sent_time, value):
    now = Temperature_db()
    now.sent_time = sent_time
    now.value = value
    db_sess = create_session()
    db_sess.add(now)
    db_sess.commit()


def add_CO2(sent_time, value):
    now = CO2_db()
    now.sent_time = sent_time
    now.value = value
    db_sess = create_session()
    db_sess.add(now)
    db_sess.commit()

