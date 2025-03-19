from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True