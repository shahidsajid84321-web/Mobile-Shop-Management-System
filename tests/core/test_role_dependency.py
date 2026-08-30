import pytest
from fastapi import HTTPException
from app.dependencies.role_dependency import require_roles

class Role: 
    def __init__(self, name): self.name = name
class User:
    def __init__(self, role): self.role = Role(role)

def test_require_roles_allows_matching_role():
    checker = require_roles("Admin")
    assert checker(User("Admin")).role.name == "Admin"

def test_require_roles_rejects_wrong_role():
    checker = require_roles("Admin")
    with pytest.raises(HTTPException) as exc:
        checker(User("Customer"))
    assert exc.value.status_code == 403
