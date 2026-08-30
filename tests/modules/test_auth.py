import pytest
from pydantic import ValidationError
from app.modules.auth.auth_schema import (
    EmailVerificationConfirm, PasswordResetConfirm, UserLogin, UserRegister,
)
from app.core.security import hash_password, verify_password


def test_register_schema_accepts_valid_user():
    user = UserRegister(full_name="Ali Khan", email="ali@example.com", phone="03001234567", password="StrongPass123")
    assert user.email == "ali@example.com"


@pytest.mark.parametrize("password", ["short", "1234567"])
def test_register_rejects_short_password(password):
    with pytest.raises(ValidationError):
        UserRegister(full_name="Ali Khan", email="ali@example.com", password=password)


def test_login_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserLogin(email="not-an-email", password="password123")


@pytest.mark.parametrize("schema", [PasswordResetConfirm, EmailVerificationConfirm])
def test_security_token_schemas_require_long_tokens(schema):
    with pytest.raises(ValidationError):
        schema(token="too-short")


def test_password_hash_round_trip():
    hashed = hash_password("StrongPass123")
    assert hashed != "StrongPass123"
    assert verify_password("StrongPass123", hashed)
    assert not verify_password("WrongPass123", hashed)
