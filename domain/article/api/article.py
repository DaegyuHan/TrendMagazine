from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from domain.article.dto.response import ArticleSchema
from domain.article.entity.article import Article
from domain.article.service.article import ArticleService
from domain.auth.service.auth import AuthService
from domain.common.dto.response.api_response import APIResponse
from domain.article.dto.request import ArticleCreateRequest
from domain.magazine.service.magazine import MagazineService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/sign-in")

router = APIRouter(prefix="/api/v1/magazine/{magazine_id}/article", tags=["Article"])

# 아티클 생성
@router.post("", status_code=201, response_model=APIResponse)
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