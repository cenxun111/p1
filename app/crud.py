# app/crud.py
from typing import List, Optional
from sqlmodel import Session, select
from .models import User
from .schemas import UserCreate, UserUpdate


class CRUDUser:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserCreate) -> User:
        db_user = User.from_orm(user)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).first()
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        user = self.session.exec(statement).first()
        return user

    def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        statement = select(User).offset(skip).limit(limit)
        users = self.session.exec(statement).all()
        return users

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
