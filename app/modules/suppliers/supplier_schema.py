from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierCreate(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=150)
    contact_person: str = Field(..., min_length=2, max_length=100)
    phone: str
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    tax_number: str | None = None
    is_active: bool = True


class SupplierUpdate(BaseModel):
    company_name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    tax_number: str | None = None
    is_active: bool | None = None


class SupplierResponse(BaseModel):
    id: int
    company_name: str
    contact_person: str
    phone: str
    email: EmailStr | None
    address: str | None
    city: str | None
    country: str | None
    tax_number: str | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
