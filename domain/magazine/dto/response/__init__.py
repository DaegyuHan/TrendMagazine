from pydantic import BaseModel


class MagazineSchema(BaseModel):
    id: int
    profile_image: str
    name: str
    description: str

    class Config:
        from_attributes = True