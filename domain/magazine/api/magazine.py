from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from domain.auth.service.auth import AuthService
from domain.common.dto.response.api_response import APIResponse
from domain.magazine.dto.request import CreateMagazineRequest
from domain.magazine.dto.response import MagazineSchema
from domain.magazine.entity.magazine import Magazine
from domain.magazine.service.magazine import MagazineService
from domain.user.service.user import UserService
from domain.user.entity.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/sign-in")

router = APIRouter(prefix="/api/v1/magazine", tags=["Magazine"])

# 매거진 생성
@router.post("")
async def create_magazine(
        request: CreateMagazineRequest,
        access_token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(),
        magazine_service: MagazineService = Depends(),
):
    user_id: int = auth_service.decode_jwt(access_token=access_token)
    magazine: Magazine = await magazine_service.create_magazine(request=request, user_id=user_id)
    data = MagazineSchema.from_orm(magazine).dict()
    return APIResponse(
        status="success",
        message="매거진 생성 완료",
        data=data
    )