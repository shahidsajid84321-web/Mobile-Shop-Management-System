import pytest
from pydantic import ValidationError
from app.modules.sales.sale_schema import SaleCreate, SaleItemCreate

def test_sale_requires_items():
    with pytest.raises(ValidationError): SaleCreate(customer_id=1, invoice_number="S-1", sale_date="2026-08-30", items=[])

def test_sale_defaults_discount_and_tax():
    s = SaleCreate(customer_id=1, invoice_number="S-1", sale_date="2026-08-30", items=[{"product_id":1,"quantity":1,"unit_price":"100"}])
    assert s.discount == 0 and s.tax == 0

def test_sale_item_rejects_non_positive_values():
    with pytest.raises(ValidationError): SaleItemCreate(product_id=1, quantity=0, unit_price=100)
    with pytest.raises(ValidationError): SaleItemCreate(product_id=1, quantity=1, unit_price=0)
