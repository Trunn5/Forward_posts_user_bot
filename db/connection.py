import os

from pyrogram import Client
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.utils.loader import config, clientManager

# Создание объекта базовой модели
Base = declarative_base()


class DefaultSpamValue(Base):
    __tablename__ = 'default_spam_value'
    value = Column(Integer, default=10, primary_key=True)


class SellChannelForward(Base):
    __tablename__ = 'forward_sell_channels'
    id = Column(String, primary_key=True)
    title = Column(String)
    interval = Column(Integer, default=None)
    @property
    def get_interval(self):
        if self.interval is None:
            return session.query(DefaultSpamValue).first().value
        else:
            return self.interval

class RentChannelForward(Base):
    __tablename__ = 'forward_rent_channels'

    id = Column(String, primary_key=True)
    title = Column(String)
    interval = Column(Integer, default=None)

    @property
    def get_interval(self):
        if self.interval is None:
            return session.query(DefaultSpamValue).first().value
        else:
            return self.interval



class SellChannelSource(Base):
    __tablename__ = 'source_sell_channels'
    id = Column(String, primary_key=True)


class RentChannelSource(Base):
    __tablename__ = 'source_rent_channels'
    id = Column(String, primary_key=True)


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(String, primary_key=True)

class UserBot(Base):
    __tablename__ = 'user_bots'

    name = Column(Integer, primary_key=True, autoincrement=True)

    session_string = Column(String)


# Создание соединения с базой данных
engine = create_engine(os.getenv('DATABASE_URL'))

# Создание таблиц в базе данных (если они еще не существуют)
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()



# Добавление начальных данных
try:
    for user in session.query(UserBot).all():
        clientManager.add_client(Client(name=f"user_bot_{user.name}", session_string=user.session_string))

    if not session.query(DefaultSpamValue).first(): session.add(DefaultSpamValue())
    if not session.query(RentChannelSource).first(): session.add(RentChannelSource(id=-1))
    if not session.query(SellChannelSource).first(): session.add(SellChannelSource(id=-1))
    for admin in config.admins:
        if not session.query(Admin).filter_by(id=str(admin)).first():
            session.add(Admin(id=str(admin)))
    session.commit()
except:
    ...

