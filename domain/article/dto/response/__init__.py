from datetime import datetime

from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: int
    content: str
    main_category: str
    created_at: datetime
    magazine_id: int
    user_id: int

    class Config:
        from_attributes = True