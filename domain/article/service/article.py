from typing import List, Tuple

from fastapi import Depends
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection import get_db
from core.database.transaction import transaction
from domain.article.dto.request import ArticleCreateRequest
from domain.article.entity.article import Article
from domain.article.repository.article import ArticleRepository
from core.config import Config
from domain.magazine.exception import MagazineNotFoundException
from domain.tag.entity.tags import Tag
from domain.magazine.repository.magazine import MagazineRepository
from domain.tag.repository.tag import TagRepository
from domain.tag.repository.tag_similarity import TagSimilarityRepository
from domain.user.exception import UserNotAuthorizedException


class ArticleService:
    def __init__(
            self,
            article_repo: ArticleRepository = Depends(),
            magazine_repo: MagazineRepository = Depends(),
            tag_repo: TagRepository = Depends(),
            tag_similarity_repo: TagSimilarityRepository = Depends(),
            db_session: AsyncSession = Depends(get_db),  # 선택적
    ):
        self.article_repo = article_repo
        self.magazine_repo = magazine_repo
        self.tag_repo = tag_repo
        self.tag_similarity_repo = tag_similarity_repo
        self.db_session = db_session  # 필요하면 사용
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

    @transaction
    async def create_article(self, request: ArticleCreateRequest, magazine_id: int, user_id: int) -> Article:
        print("Transaction started:", self.db_session.in_transaction())
        # magazine 조회
        magazine = await self.magazine_repo.get_magazine_by_magazine_id(magazine_id)
        if not magazine:
            raise MagazineNotFoundException()
        # 작성자 검증
        self.validate_magazine_id(magazine_user_id=magazine.user_id, writer_user_id=user_id)
        # ai 를 활용해 카테고리 예측
        main_category, tags = await self.categorize_content(request.content)
        # article 객체 생성
        article: Article = Article.create(request.content, main_category, magazine_id, user_id)
        # db 저장
        article: Article = await self.article_repo.save_article(article)

        await self.save_tags(article.id, tags)
        # await self.save_tag_similarities(tags)
        print("Transaction ending:", self.db_session.in_transaction())
        return article

    # OpenAI로 메인 카테고리와 상세 태그 5개를 예측
    async def categorize_content(self, content: str) -> Tuple[str, List[str]]:
        prompt = (
            "다음 콘텐츠를 읽고 적절한 메인 카테고리를 다음 항목 중에서 지정해주세요 "
            "(미술, 자동차, 디자인, 엔터테인먼트, 패션, 음식, 신발, 게임, 음악, 스포츠, 전자, 영화, 기타, 라이프스타일).\n"
            "그리고 이 콘텐츠와 관련된 상세 카테고리 3개를 제안해주세요. 상세 카테고리는 너무 상세하지 않고 최대한 간단하고 대표적인 단어로 해주세요.\n\n"
            f"콘텐츠: {content}\n\n"
            "응답 형식:\n"
            "Main Category: [카테고리]\n"
            "Tags:\n"
            "- [태그1]\n"
            "- [태그2]\n"
            "- [태그3]"
        )
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.5,
        )
        # 🔹 OpenAI의 응답을 확인
        ai_response = response.choices[0].message.content.strip()
        print("===== AI 응답 확인 =====")
        print(ai_response)  # 터미널에서 확인 가능
        print("========================")

        # 🔹 응답 파싱
        result = ai_response.split("\n")
        main_category = result[0].replace("Main Category: ", "").strip()
        tags = []

        for line in result[2:5]:  # 태그 3개만 파싱
            if line.strip():  # 빈 줄 제외
                tag = line.replace("- ", "").strip()
                tags.append(tag)
            else:
                print(f"WARNING: 잘못된 형식 -> {line}")

        return main_category, tags

    # 태그 DB 저장
    async def save_tags(self, article_id: int, tags: List[str]):
        for tag_name in tags:
            tag = await self.tag_repo.get_tag_by_name(tag_name)
            if not tag:
                tag = Tag.create(tag_name)
                tag = await self.tag_repo.save_tag(tag)
                print(f"생성: {tag_name}")
            else:
                print(f"중복: {tag_name}")
            await self.article_repo.save_article_tag(article_id, tag.id)

    # 새 태그와 기존 태그 간 유사도 계산 후 저장
    async def save_tag_similarities(self, tags_with_relevance: List[Tuple[str, float]]):
        # 기존 태그들 모두 가져오기
        existing_tags = await self.tag_repo.get_all_tags()

        # 새 태그들 이름 추출
        new_tag_names = [tag_name for tag_name, _ in tags_with_relevance]

        # 새로운 태그 이름에 대해 처리
        for new_tag_name in new_tag_names:
            # 새로운 태그 객체 찾기 (이 객체는 id와 tag_name을 갖고 있어야 함)
            new_tag = await self.tag_repo.get_tag_by_name(new_tag_name)

            if new_tag is None:
                # 태그가 존재하지 않으면 새로 생성 (필요시)
                new_tag = await self.tag_repo.save_tag(new_tag_name)

            # 기존 태그들과 비교
            for existing_tag in existing_tags:
                # 동일한 태그라면 유사도를 계산하지 않음
                if new_tag.id != existing_tag.id:
                    similarity = await self.calculate_tag_similarity(new_tag.tag_name, existing_tag.tag_name)

                    # 유사도 저장
                    await self.tag_similarity_repo.save_similarity(new_tag.id, existing_tag.id, similarity)
                    print(f"Tags: {new_tag.tag_name}, {existing_tag.tag_name} | Similarity: {similarity:.2f}")

    # OpenAI 로 두 태그의 유사도 계산
    async def calculate_tag_similarity(self, tag1: str, tag2: str) -> float:
        """OpenAI로 두 태그의 유사도를 계산"""
        prompt = (
            f"다음 두 태그의 의미적 유사도를 0~1 사이 값으로 평가해주세요:\n"
            f"태그 1: {tag1}\n"
            f"태그 2: {tag2}\n\n"
            "응답 형식: [유사도 값]"
        )
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.5,
        )
        similarity = float(response.choices[0].message.content.strip("[ ]"))
        return similarity

    # 매거진 오너와 작성자 유저 id 검증
    def validate_magazine_id(self, magazine_user_id: int, writer_user_id: int):
        if magazine_user_id != writer_user_id:
            raise UserNotAuthorizedException()