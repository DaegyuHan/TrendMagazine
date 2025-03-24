from typing import List

from fastapi import Depends
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection import get_db
from domain.article.entity.article import Article
from domain.article.entity.article_tags import ArticleTags


class ArticleRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    # 아티클 db 저장
    async def save_article(self, article: Article) -> Article:
        self.session.add(instance=article)
        await self.session.flush()
        await self.session.refresh(instance=article)
        return article

    # ArticleTags 에 태그와 연관성 저장
    async def save_article_tag(self, article_id: int, tag_id: int):
        article_tag = ArticleTags(article_id=article_id, tag_id=tag_id, relevance=0) # TODO relevance 임시로 0 설정 ( 이후 칼럼 삭제 요망 )
        self.session.add(article_tag)
        await self.session.flush()

    # async def get_article_by_id(self, article_id: int) -> Optional[Article]:
    #     result = await self.session.execute(
    #         "SELECT * FROM articles WHERE id = :id", {"id": article_id}
    #     )
    #     return result.scalars().first()


    # main_category 해당 아티클 목록 조회
    async def get_articles_by_main_category(
            self,
            main_category: str,
            offset: int,
            limit: int
    ) -> List[Article]:
        query = select(Article).where(Article.main_category == main_category).order_by(desc(Article.created_at)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        articles = result.scalars().all()
        return articles

    # main_category 해당 아티클 수 반환
    async def count_articles_by_main_category(
            self,
            main_category: str
    ) -> int:
        query = select(func.count()).where(Article.main_category == main_category)
        result = await self.session.execute(query)
        count = result.scalar() or 0  # None일 경우 0 반환
        return count