import pytest
from pydantic import ValidationError
from app.modules.inventory.inventory_schema import StockTransactionCreate

def test_inventory_in_transaction():
    x = StockTransactionCreate(product_id=1, transaction_type="IN", quantity=5, unit_price="100.00")
    assert x.quantity == 5

@pytest.mark.parametrize("data", [
    {"product_id": 0, "transaction_type": "IN", "quantity": 1, "unit_price": 1},
    {"product_id": 1, "transaction_type": "BAD", "quantity": 1, "unit_price": 1},
    {"product_id": 1, "transaction_type": "OUT", "quantity": 0, "unit_price": 1},
    {"product_id": 1, "transaction_type": "OUT", "quantity": 1, "unit_price": -1},
])
def test_inventory_rejects_invalid_transaction(data):
    with pytest.raises(ValidationError): StockTransactionCreate(**data)
