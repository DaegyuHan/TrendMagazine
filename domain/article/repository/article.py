from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from core.database.connection import get_db
from domain.article.entity.article import Article
from domain.article.entity.article_tags import ArticleTags


class ArticleRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    # 아티클 db 저장
    async def save_article(self, article: Article) -> Article:
        self.session.add(instance=article)
        await self.session.commit()
        await self.session.refresh(instance=article)
        return article

    # ArticleTags 에 태그와 연관성 저장
    async def save_post_tag(self, article_id: int, tag_id: int, relevance: float):
        article_tag = ArticleTags(article_id=article_id, tag_id=tag_id, relevance=relevance)
        self.session.add(article_tag)
        await self.session.commit()

    # async def get_article_by_id(self, article_id: int) -> Optional[Article]:
    #     result = await self.session.execute(
    #         "SELECT * FROM articles WHERE id = :id", {"id": article_id}
    #     )
    #     return result.scalars().first()