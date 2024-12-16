from sqlalchemy import create_engine  #  Позволит запускать дашу БД
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///taskmanager.db", echo=True)  #  Элемент для связи с нашей БД. В скобрах адрес БД

#  Создаем сессию для связи с БД
SessionLocal = sessionmaker(bind=engine)  #  bind=engine - параметр связи(привязка) к engine

#  Модели баз данных:
class Base(DeclarativeBase):
    pass