import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.modules.products.product_schema import ProductCreate, ProductUpdate

def test_product_create_valid(valid_product):
    p = ProductCreate(**valid_product)
    assert p.selling_price > p.purchase_price

def test_product_rejects_negative_prices(valid_product):
    valid_product["purchase_price"] = -1
    with pytest.raises(ValidationError): ProductCreate(**valid_product)

def test_product_rejects_negative_stock(valid_product):
    valid_product["stock_quantity"] = -1
    with pytest.raises(ValidationError): ProductCreate(**valid_product)

def test_product_update_is_partial():
    product = ProductUpdate(selling_price="999.99")

    assert product.selling_price == Decimal("999.99")
    assert product.name is None
    assert product.purchase_price is None
    assert product.stock_quantity is None