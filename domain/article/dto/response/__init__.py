from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True