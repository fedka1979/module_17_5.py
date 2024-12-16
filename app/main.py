from fastapi import FastAPI
from app.routers import task  #  Импортируем из папки routers файл task.py
from app.routers import user  #  Импортируем из папки routers файл user.py

app = FastAPI()

@app.get("/")  #  Главная (базовая) страница
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(user.router)  #  Это позволит подключать внешние роутеры
app.include_router(task.router)

"""
 Команда запуска
python -m uvicorn app.main:app
"""

"""
 - Для установки миграции:
pip install alembic - устанавливаем alembic

 - далее устанавливаем начальные файлы миграции в папке app текущего модуля Pydantic_4
alembic init app/migrations

 - Указать адрес вашей базы данных 
sqlalchemy.url = sqlite:///taskmanager.db в появившемся alembic.ini

 - После нужно настроить файл env.py в папке app/migrations:

from app.backend.db import Base
from app.models.user import User
from app.models.task import Task
target_metadata = Base.metadata  #  Нужно найти строчку target_metadata = None

 - В терминале запускаем команду первой миграции
alembic revision -m "message"   -  В папке app/migrations/versions появится файл версии (например a29ae040fd19_.py)

 - Выполните команду alembic upgrade head      - Создастся БД taskmanager.db в папке module_17_4

Появляется в родительской директории файл базы данных taskmanager.db, который прописывали в backend/db.py (engine)

"""