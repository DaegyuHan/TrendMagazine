from typing import Optional

from fastapi import Depends

from domain.user.entity.user import User
from domain.user.repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    def get_user_by_user_id(self, user_id: str) -> Optional[User]:
        return self.user_repo.get_user_by_user_id(int(user_id))
