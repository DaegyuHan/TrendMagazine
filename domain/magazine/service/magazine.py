from fastapi import Depends

from domain.magazine.dto.request import CreateMagazineRequest
from domain.magazine.entity.magazine import Magazine
from domain.magazine.repository.magazine import MagazineRepository

class MagazineService:
    def __init__(self, magazine_repo: MagazineRepository = Depends()):
        self.magazine_repo = magazine_repo

    async def create_magazine(self, request: CreateMagazineRequest, user_id: int) -> Magazine:
        # magazine 객체 생성
        magazine: Magazine = Magazine.create(request.profile_image, request.name, user_id)
        #db 저장
        magazine: Magazine = await self.magazine_repo.save_magazine(magazine)
        return magazine