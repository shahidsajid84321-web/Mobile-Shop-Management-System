from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import (
    require_permission,
)
from app.modules.permissions.permission_schema import (
    PermissionResponse,
)
from app.modules.permissions.permission_service import (
    PermissionService,
)
from app.modules.permissions.role_permission_schema import (
    RolePermissionResponse,
    RolePermissionUpdate,
)

from app.modules.permissions.role_permission_service import (
    RolePermissionService,
)

from app.core.constants.permissions import PermissionCode


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.get(
    "/",
    response_model=list[PermissionResponse],
)
def get_permissions(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_VIEW)
    ),
):
    return PermissionService.get_all(db)


@router.get(
    "/roles/{role_id}/permissions",
    response_model=RolePermissionResponse,
)
def get_role_permissions(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_VIEW)
    ),
):
    try:
        return RolePermissionService.get_permissions(
            db,
            role_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/roles/{role_id}/permissions",
    response_model=RolePermissionResponse,
)
def update_role_permissions(
    role_id: int,
    data: RolePermissionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_UPDATE)
    ),
):
    try:
        return RolePermissionService.update_permissions(
            db,
            role_id,
            data,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) 


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.ROLES_VIEW)
    ),
):
    try:
        return PermissionService.get_one(
            db,
            permission_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )       
