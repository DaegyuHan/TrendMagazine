from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from core.database.orm import Base

__all__ = ["User"]

from domain.user.entity.user_role import UserRole

from domain.user.entity.user_status import UserStatus



class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String(60), nullable=False)
    hashed_password = Column(String(60), nullable=False)
    nickname = Column(String(30), nullable=False)
    social_id = Column(String(60), nullable=True)
    social_provider = Column(String(60), nullable=True)
    user_status = Column(SQLEnum(UserStatus, name='user_status'), default=UserStatus.ACTIVE, nullable=False)
    user_role = Column(SQLEnum(UserRole, name='user_role'), default=UserRole.GUEST, nullable=False)

    created_at = Column(TIMESTAMP(precision=6), default=datetime.now, nullable=False)

    articles = relationship("Article", back_populates="user")

    @classmethod
    def create(cls, email: str, hashed_password: str, nickname: str):
        return cls(email=email, hashed_password=hashed_password, nickname=nickname)
