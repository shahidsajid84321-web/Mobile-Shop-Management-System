from decimal import Decimal

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StockTransactionCreate(BaseModel):
    product_id: int = Field(gt=0)
    transaction_type: Literal["IN", "OUT"]
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    remarks: str | None = None


class StockTransactionResponse(BaseModel):
    id: int
    product_id: int
    transaction_type: str
    quantity: int
    unit_price: Decimal
    remarks: str | None
    model_config = ConfigDict(
        from_attributes=True,
    )
