from fastapi import APIRouter, Depends

from domain.auth.dto.request import AuthSignUpRequest, AuthSignInRequest
from domain.auth.service.auth import AuthService
from domain.common.dto.response.api_response import APIResponse
from domain.user.dto.response import UserSchema

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# 회원가입
@router.post("/sign-up", status_code=201, response_model=APIResponse)
async def auth_sign_up_handler(
        request: AuthSignUpRequest,
        auth_service: AuthService = Depends(),
):
    user = await auth_service.sign_up(request)
    data = UserSchema.from_orm(user).dict()
    return APIResponse(
        status="success",
        message="사용자가 성공적으로 생성되었습니다",
        data=data
    )

# 로그인
@router.post("/sign-in", status_code=200, response_model=APIResponse)
async def auth_sign_in_handler(
    request: AuthSignInRequest,
    auth_service: AuthService = Depends()
):
    access_token = await auth_service.sign_in(request)
    return APIResponse(
        status="success",
        message="로그인 성공",
        data={"access_token": access_token}
    )