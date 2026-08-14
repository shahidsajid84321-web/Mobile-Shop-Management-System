from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ReturnCreate(BaseModel):
    order_id: int
    reason: str = Field(min_length=5, max_length=500)
    notes: str | None = Field(default=None, max_length=500)


class ReturnResponse(BaseModel):
    id: int
    order_id: int
    customer_id: int
    status: str
    reason: str
    refund_amount: Decimal
    notes: str | None
    created_at: datetime
    resolved_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


class ReturnStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=30)
    notes: str | None = Field(default=None, max_length=500)
