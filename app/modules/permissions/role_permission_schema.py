from pydantic import BaseModel


class RolePermissionResponse(BaseModel):
    role_id: int
    role_name: str
    permissions: list[str]


class RolePermissionUpdate(BaseModel):
    permission_ids: list[int]
