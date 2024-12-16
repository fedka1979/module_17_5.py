from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import select, insert, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")                                    # Функция для получения всех задач
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")                             # Функция для получения задачи по ID
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task


@router.post("/create")                              # Функция для создания новой задачи
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    task_slug = slugify(task.title)                  # Создание slug (перевод в нижний регистр)
    new_task = Task(
        title=task.title,
        content=task.content,
        priority=task.priority,
        user_id=user_id,
        slug=task_slug
    )
    db.execute(insert(Task).values(
        title=new_task.title,
        content=new_task.content,
        priority=new_task.priority,
        user_id=new_task.user_id,
        slug=task_slug
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")                               # Функция для обновления задачи
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    existing_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.execute(update(Task).where(Task.id == task_id).values(**task.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router.delete("/delete")                            # Функция для удаления задачи
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deleted successfully!'}


