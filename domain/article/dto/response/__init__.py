from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: int
    content: str
    category: str

    class Config:
        from_attributes = True