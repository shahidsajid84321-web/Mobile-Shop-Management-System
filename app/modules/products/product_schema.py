from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    brand: str = Field(..., min_length=2, max_length=100)
    model_number: str | None = None
    sku: str = Field(..., max_length=100)
    barcode: str | None = None
    description: str | None = None

    purchase_price: Decimal
    selling_price: Decimal

    stock_quantity: int = 0
    minimum_stock: int = 0

    image: str | None = None

    is_active: bool = True

    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    model_number: str | None = None
    sku: str | None = None
    barcode: str | None = None
    description: str | None = None

    purchase_price: Decimal | None = None
    selling_price: Decimal | None = None

    stock_quantity: int | None = None
    minimum_stock: int | None = None

    image: str | None = None

    is_active: bool | None = None

    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int

    name: str
    brand: str
    model_number: str | None
    sku: str
    barcode: str | None
    description: str | None

    purchase_price: Decimal
    selling_price: Decimal

    stock_quantity: int
    minimum_stock: int

    image: str | None

    is_active: bool

    category_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
