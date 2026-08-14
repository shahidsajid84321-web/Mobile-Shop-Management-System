from pydantic import ValidationError

from app.modules.store.store_schema import CheckoutRequest
from app.modules.store.return_schema import ReturnCreate, ReturnStatusUpdate


def test_checkout_schema_rejects_negative_shipping():
    try:
        CheckoutRequest(
            delivery_name="Ali",
            delivery_phone="03001234567",
            delivery_address="123 Main Street",
            delivery_city="Lahore",
            shipping_fee=-1,
        )
    except ValidationError:
        return
    raise AssertionError("negative shipping_fee should fail validation")


def test_return_schema_validation():
    item = ReturnCreate(order_id=1, reason="Device arrived damaged")
    assert item.order_id == 1
    update = ReturnStatusUpdate(status="Approved")
    assert update.status == "Approved"
