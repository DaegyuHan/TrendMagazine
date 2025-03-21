from pydantic import BaseModel, Field


class CreateMagazineRequest(BaseModel):
    profile_image: str = Field(..., examples=["http://image url"])
    name: str = Field(..., examples=["Magazine Name"])

    class Config:
        from_attributes = True