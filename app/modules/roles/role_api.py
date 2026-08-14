from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import (
    require_permission,
)
from app.modules.roles.role_schema import (
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)
from app.modules.roles.role_service import RoleService

from app.core.constants.permissions import PermissionCode


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.post(
    "/",
    response_model=RoleResponse,
    status_code=201,
)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_CREATE)
    ),
):
    try:
        return RoleService.create(
            db,
            role,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[RoleResponse],
)
def get_roles(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_VIEW)
    ),
):
    return RoleService.get_all(db)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_VIEW)
    ),
):
    try:
        return RoleService.get_one(
            db,
            role_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
)
def update_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_UPDATE)
    ),
):
    try:
        return RoleService.update(
            db,
            role_id,
            role,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{role_id}",
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_DELETE)
    ),
):
    try:
        RoleService.delete(
            db,
            role_id,
        )

        return {
            "message": "Role deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )