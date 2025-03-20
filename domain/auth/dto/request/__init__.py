from pydantic import BaseModel, Field

class AuthSignUpRequest(BaseModel):
    email: str = Field(..., examples=["admin@test.com"])
    password: str = Field(..., examples=["1234"])
    nickname: str = Field(..., examples=["닉네임"])

class AuthSignInRequest(BaseModel):
    email: str = Field(..., examples=["admin@test.com"])
    password: str = Field(..., examples=["1234"])