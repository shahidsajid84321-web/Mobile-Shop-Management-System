import pytest
from pydantic import ValidationError
from app.modules.permissions.role_permission_schema import RolePermissionUpdate

def test_role_permission_update_accepts_ids():
    x = RolePermissionUpdate(permission_ids=[1, 2, 3])
    assert x.permission_ids == [1, 2, 3]

def test_role_permission_update_requires_list():
    with pytest.raises(ValidationError): RolePermissionUpdate(permission_ids="1")
