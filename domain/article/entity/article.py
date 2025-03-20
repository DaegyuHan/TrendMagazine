from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from core.database.orm import Base

__all__ = ["Article"]

class Article(Base):
    __tablename__ = "article"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(precision=6), default=datetime.now, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="articles")

    @classmethod
    def create(cls, content: str, user_id: int):
        return cls(content=content, user_id=user_id)