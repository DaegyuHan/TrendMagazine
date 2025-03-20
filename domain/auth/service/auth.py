import bcrypt
from fastapi import Depends, HTTPException
from jose import jwt
from datetime import datetime, timedelta

from domain.auth.dto.request import AuthSignUpRequest, AuthSignInRequest
from domain.auth.exception import NotAuthorizedException
from domain.user.entity.user import User
from domain.user.exception import UserNotFoundException, DuplicateEmailException
from domain.user.repository.user import UserRepository
from core.config import Config



class AuthService:
    encoding: str = "UTF-8"
    secret_key: str = Config.JWT_SECRET_KEY
    jwt_algorithm: str = "HS256"

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def sign_up(self, request: AuthSignUpRequest) -> User:
        # email 중복검사
        existing_user: User = await self.user_repo.get_user_by_email(email=request.email)
        if existing_user:
            raise DuplicateEmailException()
        # pw hashing
        hashed_password: str = self.hash_password(plain_password=request.password)
        # user 객체 생성
        user: User = User.create(email=request.email, hashed_password=hashed_password, nickname=request.nickname)
        # db 저장
        user = await self.user_repo.save_user(user)
        return user

    async def sign_in(self, request: AuthSignInRequest) -> str:
        # email 확인
        user: User | None = await self.user_repo.get_user_by_email(email=request.email)
        if not user:
            raise UserNotFoundException()

        # 비밀번호 확인
        verified: bool = self.verify_password(
            plain_password=request.password,
            hashed_password= user.hashed_password,
        )
        if not verified:
            raise NotAuthorizedException()

        # access token 발급
        access_token: str = self.create_jwt(id=user.id)

        return access_token


    def hash_password(self, plain_password: str) -> str:
        hashed_password=bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, id: int) -> str:
        return jwt.encode(
            {
                "sub": id,    # unique id
                "exp": datetime.now() + timedelta(days=1),  # 시간 하루 유효
            },
            self.secret_key,
            algorithm=self.jwt_algorithm)

    def decode_jwt(self, access_token: str):
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # expire
        return payload["sub"]   # username