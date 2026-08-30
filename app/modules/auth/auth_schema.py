from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    password: str = Field(..., min_length=8, max_length=100)


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
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str | None = None


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=20, max_length=200)
    new_password: str = Field(..., min_length=8, max_length=100)


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    token: str = Field(..., min_length=20, max_length=200)
