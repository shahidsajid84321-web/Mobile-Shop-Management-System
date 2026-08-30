from datetime import timedelta
from jose import jwt
from app.core.auth import create_access_token, create_refresh_token, hash_token
from app.core.config import settings


def test_access_token_contains_security_claims():
    token, jti, expires = create_access_token({"sub": "123", "role": "Admin"}, timedelta(minutes=5))
    claims = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert claims["sub"] == "123"
    assert claims["role"] == "Admin"
    assert claims["type"] == "access"
    assert claims["jti"] == jti
    assert expires.timestamp() > claims["iat"]


def test_refresh_token_is_opaque_and_only_hash_is_stored():
    token, token_hash, expires = create_refresh_token()
    assert len(token) > 50
    assert token != token_hash
    assert hash_token(token) == token_hash
    assert expires is not None
