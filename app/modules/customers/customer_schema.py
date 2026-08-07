from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str = Field(..., min_length=11, max_length=20)
    address: str | None = None


class CustomerUpdate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str = Field(..., min_length=11, max_length=20)
    address: str | None = None
    is_active: bool


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr | None
    phone: str
    address: str | None
    is_active: bool

    model_config = {"from_attributes": True}
