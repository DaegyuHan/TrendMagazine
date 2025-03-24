from typing import Callable
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection import AsyncSessionFactory


def transaction(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        # 세션이 이미 있으면 사용, 없으면 새로 열기
        db_session = getattr(self, 'db_session', None)
        if db_session is None:
            async with AsyncSessionFactory() as db_session:
                self.db_session = db_session  # 임시로 할당
                async with db_session.begin():
                    result = await func(self, *args, **kwargs)
                return result
        else:
            async with self.db_session.begin():
                result = await func(self, *args, **kwargs)
            return result
    return wrapper