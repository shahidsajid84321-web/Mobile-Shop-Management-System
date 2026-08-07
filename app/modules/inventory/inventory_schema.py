from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class StockTransactionCreate(BaseModel):
    product_id: int
    transaction_type: str
    quantity: int
    unit_price: Decimal
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
