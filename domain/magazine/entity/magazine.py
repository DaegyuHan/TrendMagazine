from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP


__all__ = ["Magazine"]

from sqlalchemy.orm import relationship

from core.database.orm import Base


class Magazine(Base):
    __tablename__ = "magazines"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    profile_image = Column(String(255), nullable=False)
    name = Column(String(60), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP(), default=datetime.now, nullable=False)
    updated_at = Column(TIMESTAMP(), default=datetime.now, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    articles = relationship("Article", back_populates="magazine")

    @classmethod
    def create(cls, name:str, profile_image:str, user_id:int) -> "Magazine":
        return cls(name=name, profile_image=profile_image, user_id=user_id)