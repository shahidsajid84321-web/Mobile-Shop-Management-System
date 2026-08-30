import pytest
from pydantic import ValidationError
from app.modules.payments.payment_schema import PaymentCreate
from app.modules.payments.payment_event_schema import PaymentWebhookRequest

def test_payment_create_valid():
    p = PaymentCreate(sale_id=1, amount="500.00", payment_method="Cash", payment_date="2026-08-30")
    assert str(p.amount) == "500.00"

def test_payment_rejects_non_positive_amount():
    with pytest.raises(ValidationError): PaymentCreate(sale_id=1, amount=0, payment_method="Cash", payment_date="2026-08-30")

def test_webhook_requires_event_fields():
    w = PaymentWebhookRequest(provider="Stripe", event_id="evt_1", event_type="payment.succeeded")
    assert w.payload is None
