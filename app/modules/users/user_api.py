from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import (
    require_permission,
)
from app.modules.users.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.modules.users.user_service import UserService

from app.shared.common_schema import ApiResponse

from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
    pagination_params,
)

from app.shared.responses import success_response

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=ApiResponse[UserResponse],
    status_code=201,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.USERS_CREATE)
    ),
):
    try:
        created_user = UserService.create(
            db,
            user,
            current_user,
        )

        return ApiResponse(
            success=True,
            message="User created successfully.",
            data=created_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=ApiResponse[
        PaginatedResponse[UserResponse]
    ],
)
def get_users(
    pagination: PaginationParams = Depends(
        pagination_params
    ),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.USERS_VIEW)
    ),
):
    page = pagination.page
    page_size = pagination.page_size

    data = UserService.get_paginated(
        db,
        page,
        page_size,
    )

    return success_response(
        message="Users retrieved successfully.",
        data=data,
    )


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.USERS_VIEW)
    ),
):
    try:
        found_user = UserService.get_one(
            db,
            user_id,
        )

        return ApiResponse(
            success=True,
            message="User retrieved successfully.",
            data=found_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.USERS_UPDATE)
    ),
):
    try:
        updated_user = UserService.update(
            db,
            user_id,
            user,
            current_user,
        )

        return ApiResponse(
            success=True,
            message="User updated successfully.",
            data=updated_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{user_id}",
    response_model=ApiResponse[None],
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.USERS_DELETE)
    ),
):
    try:
        UserService.delete(
            db,
            user_id,
            current_user,
        )

        return ApiResponse(
            success=True,
            message="User deleted successfully.",
            data=None,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
