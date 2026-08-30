import pytest
from pydantic import ValidationError
from app.modules.roles.role_schema import RoleCreate, RoleUpdate

def test_role_create_valid():
    assert RoleCreate(name="Manager").name == "Manager"

def test_role_name_min_length():
    with pytest.raises(ValidationError): RoleCreate(name="A")

def test_role_update_partial():
    assert RoleUpdate(description="Can manage inventory").description == "Can manage inventory"
