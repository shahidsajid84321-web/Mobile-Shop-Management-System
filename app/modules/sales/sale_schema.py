from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)


class SaleCreate(BaseModel):
    customer_id: int

    invoice_number: str = Field(
        min_length=1,
        max_length=100,
    )

    sale_date: date

    discount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )

    tax: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )

    remarks: str | None = None

    items: list[SaleItemCreate] = Field(
        min_length=1,
    )


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    cost_price: Decimal
    subtotal: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


class SaleResponse(BaseModel):
    id: int
    customer_id: int
    invoice_number: str
    sale_date: date
    total_amount: Decimal
    discount: Decimal
    tax: Decimal
    grand_total: Decimal
    payment_status: str
    remarks: str | None
    items: list[SaleItemResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )
