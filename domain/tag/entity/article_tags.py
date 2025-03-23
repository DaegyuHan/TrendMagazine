from sqlalchemy import Column, Integer, Float, ForeignKey

from core.database.orm import Base


class ArticleTags(Base):
    __tablename__ = "article_tags"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, index=True)  # Article 테이블 참조
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False, index=True)  # Tags 테이블 참조
    relevance = Column(Float, nullable=False)  # 연관성 (0~1)