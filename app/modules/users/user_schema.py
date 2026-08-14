from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = None

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
    )

    role_id: int

    is_active: bool = True


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: EmailStr | None = None

    phone: str | None = None

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100,
    )

    role_id: int | None = None

    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    is_active: bool
    role_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )