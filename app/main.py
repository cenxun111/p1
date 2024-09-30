# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlmodel import SQLModel, Session
from .database import engine, get_session
from .models import User
from .schemas import UserCreate, UserRead, UserUpdate
from .crud import CRUDUser

app = FastAPI(title="FastAPI SQLModel PostgreSQL CRUD 示例")

# 创建所有数据库表
SQLModel.metadata.create_all(engine)


@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    crud = CRUDUser(session)
    # 检查邮箱是否已存在
    existing_user = crud.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    db_user = crud.create_user(user)
    return db_user


@app.get("/users/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    crud = CRUDUser(session)
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    crud = CRUDUser(session)
    user = crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)
):
    crud = CRUDUser(session)
    user = crud.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    crud = CRUDUser(session)
    success = crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户未找到")
    return
