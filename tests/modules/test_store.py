import pytest
from pydantic import ValidationError
from app.modules.store.store_schema import CartItemRequest, CheckoutRequest, OrderStatusUpdate
from app.modules.store.return_schema import ReturnCreate, ReturnStatusUpdate

def test_cart_quantity_limits():
    assert CartItemRequest(product_id=1, quantity=1000).quantity == 1000
    with pytest.raises(ValidationError): CartItemRequest(product_id=1, quantity=0)
    with pytest.raises(ValidationError): CartItemRequest(product_id=1, quantity=1001)

def test_checkout_rejects_negative_shipping():
    with pytest.raises(ValidationError): CheckoutRequest(delivery_name="Ali", delivery_phone="03001234567", delivery_address="123 Main Street", delivery_city="Lahore", shipping_fee=-1)

def test_order_and_return_status_validation():
    assert OrderStatusUpdate(status="Shipped").status == "Shipped"
    assert ReturnCreate(order_id=1, reason="Device arrived damaged").order_id == 1
    with pytest.raises(ValidationError): ReturnStatusUpdate(status="")
