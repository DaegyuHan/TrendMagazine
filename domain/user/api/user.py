from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from domain.common.dto.response.api_response import APIResponse
from domain.user.dto.response import UserSchema
from domain.user.service.user import UserService
from domain.auth.service.auth import AuthService
from domain.user.entity.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/sign-in")

router = APIRouter(prefix="/api/v1/users", tags=["User"])

# 내 프로필 조회
@router.get("/me")
async def get_my_profile(
        access_token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(),
        user_service: UserService = Depends(),
):
    user_id: int = auth_service.decode_jwt(access_token=access_token)
    user: User = await user_service.get_user_by_user_id(user_id=user_id)
    data = UserSchema.from_orm(user).dict()
    return APIResponse(
        status="success",
        message="내 프로필 조회 완료",
        data=data
    )

# 다른 사람 조회
@router.get("/{user_id}")
async def get_user_profile(
        user_id: int,
        user_service: UserService = Depends(),
):
    user: User = await user_service.get_user_by_user_id(user_id=user_id)
    data = UserSchema.from_orm(user).dict()
    return APIResponse(
        status="success",
        message="유저 프로필 조회 완료",
        data=data
    )