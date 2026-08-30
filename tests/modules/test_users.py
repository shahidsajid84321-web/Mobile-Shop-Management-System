import pytest
from pydantic import ValidationError
from app.modules.users.user_schema import UserCreate, UserUpdate

def test_user_create_valid():
    u = UserCreate(full_name="Admin User", email="admin@example.com", password="StrongPass123", role_id=1)
    assert u.is_active is True

def test_user_create_rejects_short_password():
    with pytest.raises(ValidationError): UserCreate(full_name="Admin", email="admin@example.com", password="short", role_id=1)

def test_user_update_can_change_only_role():
    assert UserUpdate(role_id=2).role_id == 2
