from sqlalchemy import Column, Integer, String

from core.database.orm import Base


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)  # tag_id
    tag_name = Column(String, unique=True, nullable=False, index=True)  # 태그 이름

    @classmethod
    def create(cls, tag_name: str) -> "Tag":
        return cls(tag_name=tag_name)