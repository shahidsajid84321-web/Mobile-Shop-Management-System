from pydantic import BaseModel, Field


class PaymentWebhookRequest(BaseModel):
    provider: str = Field(min_length=2, max_length=50)
    event_id: str = Field(min_length=2, max_length=150)
    event_type: str = Field(min_length=2, max_length=100)
    payload: dict | None = None
