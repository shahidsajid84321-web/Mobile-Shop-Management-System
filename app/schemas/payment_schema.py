from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    sale_id: int
    amount: Decimal = Field(gt=0)
    payment_method: str
    payment_date: date
    reference_number: str | None = None
    remarks: str | None = None


class PaymentResponse(BaseModel):
    id: int
    sale_id: int
    amount: Decimal
    payment_method: str
    payment_date: date
    reference_number: str | None
    remarks: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )