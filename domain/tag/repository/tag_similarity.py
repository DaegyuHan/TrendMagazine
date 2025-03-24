from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.database.connection import get_db
from domain.tag.entity.tag_similarity import TagSimilarity


class TagSimilarityRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    # 태그 유사도 저장
    async def save_similarity(self, tag_id_1: int, tag_id_2: int, similarity: float):
        # 중복 체크 (tag_id_1, tag_id_2 양방향 확인)
        existing = await self.get_similarity(tag_id_1, tag_id_2)
        if not existing:
            tag_similarity = TagSimilarity.create(tag_id_1, tag_id_2, similarity)
            self.session.add(tag_similarity)
            await self.session.commit()

    # 태그가 이미 저장되어있는지 조회
    async def get_similarity(self, tag_id_1: int, tag_id_2: int) -> Optional[TagSimilarity]:
        from sqlalchemy import text
        result = await self.session.execute(text(
            "SELECT * FROM tag_similarities WHERE "
            "(tag_id_1 = :tag1 AND tag_id_2 = :tag2) OR (tag_id_1 = :tag2 AND tag_id_2 = :tag1)"),
            {"tag1": tag_id_1, "tag2": tag_id_2}
        )
        return result.scalars().first()