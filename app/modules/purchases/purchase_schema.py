from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)


class PurchaseCreate(BaseModel):
    supplier_id: int
    invoice_number: str = Field(
        min_length=1,
        max_length=100,
    )
    purchase_date: date
    remarks: str | None = None
    items: list[PurchaseItemCreate] = Field(
        min_length=1,
    )

class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    invoice_number: str
    purchase_date: date
    total_amount: Decimal
    remarks: str | None
    items: list[PurchaseItemResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )
