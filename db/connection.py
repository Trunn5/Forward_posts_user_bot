import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Создание объекта базовой модели
Base = declarative_base()


class DefaultSpamValue(Base):
    __tablename__ = 'default_spam_value'
    value = Column(Integer, default=10, primary_key=True)


class SellChannelForward(Base):
    __tablename__ = 'forward_sell_channels'
    id = Column(String, primary_key=True)
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


# Создание соединения с базой данных
engine = create_engine(os.getenv('DATABASE_URL'))

# Создание таблиц в базе данных (если они еще не существуют)
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()


