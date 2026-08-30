import pytest
from pydantic import ValidationError
from app.modules.purchases.purchase_schema import PurchaseCreate, PurchaseItemCreate

def test_purchase_requires_at_least_one_item():
    with pytest.raises(ValidationError): PurchaseCreate(supplier_id=1, invoice_number="P-1", purchase_date="2026-08-30", items=[])

def test_purchase_item_rejects_non_positive_quantity_or_price():
    with pytest.raises(ValidationError): PurchaseItemCreate(product_id=1, quantity=0, unit_price=10)
    with pytest.raises(ValidationError): PurchaseItemCreate(product_id=1, quantity=1, unit_price=0)
