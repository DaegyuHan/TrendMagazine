from fastapi import Depends
from sqlalchemy.orm import Session

from core.database.connection import get_db
from domain.magazine.entity.magazine import Magazine


class MagazineRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def save_magazine(self, magazine: Magazine) -> Magazine:
        self.session.add(instance=magazine)
        await self.session.commit()
        await self.session.refresh(instance=magazine)
        return magazine

    def get_magazine_by_magazine_id(self, magazine_id: int) -> Magazine:
        from sqlalchemy import select
        return self.session.scalar(select(Magazine).where(Magazine.id == magazine_id))