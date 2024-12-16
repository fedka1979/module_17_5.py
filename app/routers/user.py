from fastapi import APIRouter, Depends, status, HTTPException      # Сессия БД
from sqlalchemy.orm import Session                                 # Функция подключения к БД
from app.backend.db_depends import get_db                          # Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.user import User
from app.models.task import Task
from app.schemas import CreateUser, UpdateUser                     # Функции работы с записями.
from sqlalchemy import insert, select, update, delete              # Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")                        #  Возвращает список всех пользователей из базы данных
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users

@router.get("/user_id")                 #  Извлекает пользователя по user_id и возвращает его
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create")                 #  Добавляет нового пользователя в базу данных
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user_slug = slugify(user.username)         # Создание slug (перевод в нижний регистр)
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=user_slug
    )
    db.execute(insert(User).values(
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        age=new_user.age,
        slug = user_slug
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")                  #  Обновляет данные пользователя, если он найден
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(**user.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete")                #  Удаляет пользователя по user_id
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(Task).where(Task.user_id == user_id))  # Удаление всех задач, связанных с пользователем
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted successfully!'}