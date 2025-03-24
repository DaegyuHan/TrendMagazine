from sqlalchemy import Column, Integer, Float, ForeignKey

from core.database.orm import Base


class TagSimilarity(Base):
    __tablename__ = "tag_similarities"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)  # 유사도 레코드 ID
    tag_id_1 = Column(Integer, ForeignKey("tags.id"), nullable=False, index=True)  # 첫 번째 태그
    tag_id_2 = Column(Integer, ForeignKey("tags.id"), nullable=False, index=True)  # 두 번째 태그
    similarity = Column(Float, nullable=False)  # 유사도 (0~1)

    @classmethod
    def create(cls, tag_id_1: int, tag_id_2: int, similarity: float) -> "TagSimilarity":
        return cls(tag_id_1=tag_id_1, tag_id_2=tag_id_2, similarity=similarity)