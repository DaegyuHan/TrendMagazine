import bcrypt
from fastapi import Depends
from openpyxl.utils.protection import hash_password

from domain.auth.dto.request import AuthSignUpRequest
from domain.user.entity.user import User
from domain.user.repository.user import UserRepository


class AuthService:
    encoding: str = "UTF-8"
    secret_key: str = "3a86045e90623055658008024ff4e09577f177f9a5173c9eb4ac39223a675d21"
    jwt_algorithm: str = "HS256"

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def sign_up(self, request: AuthSignUpRequest) -> User:
        hashed_password: str = self.hash_password(plain_password=request.password)
        user: User = User.create(username=request.username, hashed_password=hashed_password)
        user = await self.user_repo.save_user(user)
        return user

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