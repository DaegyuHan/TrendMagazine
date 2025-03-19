from pydantic import BaseModel, Field

class AuthSignUpRequest(BaseModel):
    email: str = Field(..., examples=["admin@test.com"])
    password: str = Field(..., examples=["1234"])

class AuthSignInRequest(BaseModel):
    email: str = Field(..., examples=["admin@test.com"])
    password: str = Field(..., examples=["1234"])