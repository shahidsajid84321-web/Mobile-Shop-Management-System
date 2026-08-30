import os
import pytest

# Keep unit/contract tests independent from the developer's local .env/MySQL server.
os.environ.setdefault("APP_NAME", "Mobile Shop Test")
os.environ.setdefault("APP_VERSION", "test")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_NAME", "mobile_shop_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only-32-chars")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault("TRUSTED_HOSTS", "testserver,localhost")
os.environ.setdefault("ALLOW_PUBLIC_REGISTRATION", "true")

@pytest.fixture
def valid_product():
    return {
        "name": "iPhone 15", "brand": "Apple", "model_number": "A3090",
        "sku": "IPH15-128", "barcode": "1234567890123", "description": "128GB smartphone",
        "purchase_price": "150000.00", "selling_price": "175000.00",
        "stock_quantity": 10, "minimum_stock": 2, "is_active": True, "category_id": 1,
    }
