from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP

from core.database.orm import Base

__all__ = ["User"]

class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String(60), nullable=False)
    hashed_password = Column(String(60), nullable=False)
    social_id = Column(String(60), nullable=True)
    social_provider = Column(String(60), nullable=True)
    created_at = Column(TIMESTAMP(precision=6), default=datetime.now(), nullable=False)

    @classmethod
    def create(cls, email: str, hashed_password: str):
        return cls(email=email, hashed_password=hashed_password)
