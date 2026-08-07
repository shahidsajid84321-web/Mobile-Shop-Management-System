from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    password: str = Field(..., min_length=8, max_length=100)
    role_id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    role_id: int

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
