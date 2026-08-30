import pytest
from pydantic import ValidationError
from app.modules.suppliers.supplier_schema import SupplierCreate

def test_supplier_create_valid():
    s = SupplierCreate(company_name="ABC Traders", contact_person="Ali Khan", phone="03001234567", email="sales@abc.com")
    assert s.is_active is True

def test_supplier_rejects_invalid_email():
    with pytest.raises(ValidationError): SupplierCreate(company_name="ABC", contact_person="Ali", phone="03001234567", email="bad")
