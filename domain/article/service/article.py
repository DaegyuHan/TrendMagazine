from fastapi import Depends

from domain.article.dto.request import ArticleCreateRequest
from domain.article.entity.article import Article
from domain.article.repository.article import ArticleRepository


class ArticleService:
    def __init__(self,article_repo: ArticleRepository = Depends(),):
        self.article_repo = article_repo

    async def create_article(self, request: ArticleCreateRequest, user_id: int) -> Article:
        # article 객체 생성
        article: Article = Article.create(request.content, user_id)
        # db 저장
        article: Article = await self.article_repo.save_article(article)
        return article