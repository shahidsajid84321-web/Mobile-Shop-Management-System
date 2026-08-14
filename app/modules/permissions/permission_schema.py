from pydantic import BaseModel, ConfigDict


class PermissionResponse(BaseModel):
    id: int
    name: str
    code: str
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )