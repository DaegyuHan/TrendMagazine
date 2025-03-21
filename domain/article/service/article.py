from fastapi import Depends
from openai import OpenAI

from domain.article.dto.request import ArticleCreateRequest
from domain.article.entity.article import Article
from domain.article.repository.article import ArticleRepository
from core.config import Config


class ArticleService:
    def __init__(self,article_repo: ArticleRepository = Depends(),):
        self.article_repo = article_repo
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def create_article(self, request: ArticleCreateRequest, user_id: int) -> Article:
        # ai 를 활용해 카테고리 예측
        category = await self.categorize_content(request.content)
        # article 객체 생성
        article: Article = Article.create(request.content, category, user_id)
        # db 저장
        article: Article = await self.article_repo.save_article(article)
        return article

    async def categorize_content(self, content: str) -> str:
        """OpenAI를 사용해 콘텐츠의 카테고리를 예측"""
        prompt = (
            "다음 콘텐츠를 읽고 적절한 카테고리를 다음 항목 중에서 지정해주세요 (미술, 자동차, 디자인, 엔터테인먼트, 패션, 음식, 신발, 게임, 음악, 스포츠, 전자, 영화, 기타, 라이프스타일):\n\n"
            f"{content}"
        )
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.5,
        )
        category = response.choices[0].message.content.strip()
        return category