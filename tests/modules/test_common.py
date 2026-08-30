from app.modules.permissions.permission_schema import PermissionResponse
from app.modules.permissions.role_permission_schema import RolePermissionResponse

def test_permission_response_shape():
    p = PermissionResponse(id=1, name="Products", code="products.read", description=None)
    assert p.code == "products.read"

def test_role_permissions_response_shape():
    r = RolePermissionResponse(role_id=1, role_name="Admin", permissions=["products.read"])
    assert r.permissions == ["products.read"]
