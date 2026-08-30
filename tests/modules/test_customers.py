import pytest
from pydantic import ValidationError
from app.modules.customers.customer_schema import CustomerCreate, CustomerUpdate

def test_customer_create_valid():
    c = CustomerCreate(full_name="Ali Khan", email="ali@example.com", phone="03001234567")
    assert c.phone == "03001234567"

def test_customer_rejects_invalid_email():
    with pytest.raises(ValidationError): CustomerCreate(full_name="Ali Khan", email="bad", phone="03001234567")

def test_customer_update_requires_active_flag():
    with pytest.raises(ValidationError): CustomerUpdate(full_name="Ali", phone="03001234567")
