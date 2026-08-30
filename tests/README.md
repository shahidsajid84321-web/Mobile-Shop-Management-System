# Backend Test Suite

Run from the backend directory:

```bash
pip install -r requirements.txt
pytest
```

Run one module independently:

```bash
pytest tests/modules/test_products.py
pytest tests/modules/test_sales.py
pytest tests/modules/test_auth.py
```

Run a single test:

```bash
pytest tests/modules/test_auth.py::test_password_hash_round_trip
```

## What is covered

- Authentication schemas, password hashing, JWT/refresh-token helpers
- Login request rate-limit middleware
- Role authorization dependency
- Categories
- Products
- Inventory
- Suppliers
- Purchases
- Customers
- Sales
- Payments and payment webhook schema
- Dashboard response schema
- Reports
- Roles and permissions
- Users
- Online store/cart/checkout/order/return schemas
- OpenAPI endpoint contract checks

These tests intentionally avoid requiring a live MySQL database for the unit/schema/contract tests. Database CRUD and full end-to-end tests should be run against a dedicated test database separately.
