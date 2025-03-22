from pydantic import BaseModel, Field

class CreateArticleRequest(BaseModel):
    content: str = Field(..., examples=["content"])

    class Config:
        from_attributes = True