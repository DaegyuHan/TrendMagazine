from typing import Optional, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import text, select

from core.database.connection import get_db
from domain.tag.entity.tags import Tag
from domain.tag.entity.tag_similarity import TagSimilarity

class TagRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    # 태그 이름으로 조회
    async def get_tag_by_name(self, tag_name: str) -> Optional[Tag]:
        result = await self.session.execute(select(Tag).where(Tag.tag_name == tag_name))
        return result.scalars().first()

    # 새 태그 저장
    async def save_tag(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        await self.session.refresh(instance=tag)
        return tag

    # 모든 태그 조회
    async def get_all_tags(self) -> List[Tag]:
        result = await self.session.execute(select(Tag))
        return result.scalars().all()