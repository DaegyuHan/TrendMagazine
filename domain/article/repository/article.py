from fastapi import Depends
from sqlalchemy.orm import Session
from core.database.connection import get_db
from domain.article.entity.article import Article


class ArticleRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def save_article(self, article: Article) -> Article:
        self.session.add(instance=article)
        await self.session.commit()
        await self.session.refresh(instance=article)
        return article