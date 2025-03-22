from pydantic import BaseModel


class MagazineSchema(BaseModel):
    id: int
    profile_image: str
    name: str
    description: str | None

    class Config:
        from_attributes = True