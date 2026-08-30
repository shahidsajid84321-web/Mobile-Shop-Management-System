from app.main import app


def test_health_endpoint_is_documented():
    spec = app.openapi()
    paths = spec["paths"]

    assert "/healthz" in paths
    assert "get" in paths["/healthz"]


def test_health_endpoint_has_expected_response():
    spec = app.openapi()

    health = spec["paths"]["/healthz"]["get"]

    assert health["responses"]["200"]


def test_openapi_documents_core_auth_endpoints():
    spec = app.openapi()
    paths = spec["paths"]

    expected_endpoints = [
        "/auth/register",
        "/auth/login",
        "/auth/refresh",
        "/auth/logout",
        "/auth/password-reset/request",
        "/auth/password-reset/confirm",
        "/auth/email-verification/verify",
        "/auth/email-verification/resend",
        "/auth/me",
        "/auth/admin-test",
    ]

    for endpoint in expected_endpoints:
        assert endpoint in paths, (
            f"Missing documented authentication endpoint: {endpoint}"
        )


def test_openapi_contains_business_modules():
    spec = app.openapi()
    paths = spec["paths"]

    expected_prefixes = [
        "/categories",
        "/products",
        "/inventory",
        "/suppliers",
        "/purchases",
        "/customers",
        "/sales",
        "/payments",
        "/dashboard",
        "/reports",
        "/roles",
        "/users",
        "/permissions",
        "/store",
    ]

    for prefix in expected_prefixes:
        assert any(
            path.startswith(prefix) for path in paths
        ), f"No OpenAPI route found for module: {prefix}"


def test_openapi_contains_upload_api():
    spec = app.openapi()
    paths = spec["paths"]

    assert "/upload/product-image" in paths
    assert "post" in paths["/upload/product-image"]


def test_openapi_has_expected_metadata():
    spec = app.openapi()

    assert "openapi" in spec
    assert "info" in spec
    assert spec["info"]["title"]
    assert spec["info"]["version"]
