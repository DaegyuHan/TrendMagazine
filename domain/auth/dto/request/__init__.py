from pydantic import BaseModel, Field

class AuthSignUpRequest(BaseModel):
    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["1234"])

class AuthSignInRequest(BaseModel):
    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["1234"])