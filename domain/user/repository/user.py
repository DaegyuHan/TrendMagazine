from fastapi import Depends
from sqlalchemy.orm import Session

from core.database.connection import get_db
from domain.user.entity.user import User


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        await self.session.commit()
        await self.session.refresh(instance=user)
        return user

    def get_user_by_email(self, email: str) -> User:
        from sqlalchemy import select
        return self.session.scalar(select(User).where(User.email == email))

    def get_user_by_user_id(self, user_id: int) -> User:
        from sqlalchemy import select
        return self.session.scalar(select(User).where(User.id == user_id))