from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Query

from domain.article.dto.response import ArticleSchema
from domain.article.entity.article import Article
from domain.article.service.article import ArticleService
from domain.auth.service.auth import AuthService
from domain.common.dto.response.api_response import APIResponse
from domain.article.dto.request import ArticleCreateRequest
from domain.magazine.service.magazine import MagazineService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/sign-in")

router = APIRouter(prefix="/api/v1", tags=["Article"])

# 아티클 생성
@router.post("/magazine/{magazine_id}/article", status_code=201, response_model=APIResponse)
async def article_create_handler(
        magazine_id: int,
        request: ArticleCreateRequest,
        access_token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(),
        article_service: ArticleService = Depends(),
):
    user_id: int = auth_service.decode_jwt(access_token=access_token)
    article: Article = await article_service.create_article(request=request,  magazine_id=magazine_id, user_id=user_id)
    data = ArticleSchema.from_orm(article).dict()

    return APIResponse(
        status="success",
        message="아티클 등록 완료",
        data=data
    )


# 아티클 조회 (main_category 기준)
@router.get("/articles", status_code=200, response_model=APIResponse)
async def get_article_list_handler(
        main_category: str,
        page: int = 1,
        limit: int = 10,
        article_service: ArticleService = Depends(),
):
    # 아티클 목록 조회
    articles, total = await article_service.get_articles_by_main_category(
        main_category=main_category,
        page=page,
        limit=limit
    )

    # 응답 데이터 준비
    data = {
        "articles": [ArticleSchema.from_orm(article).dict() for article in articles],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit  # 전체 페이지 수 계산
    }

    return APIResponse(
        status="success",
        message=f"{main_category} 카테고리의 아티클 목록 조회 완료",
        data=data
    )