from pydantic import BaseModel, Field

class ArticleCreateRequest(BaseModel):
    content: str = Field(..., examples=["content"])

    class Config:
        from_attributes = True