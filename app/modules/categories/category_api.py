from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.categories.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.modules.categories.category_service import CategoryService
from app.modules.permissions.permission_dependencies import (
    require_permission,
)

from app.shared.common_schema import ApiResponse
from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
)
from app.shared.responses import success_response


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.CATEGORIES_CREATE)
    ),
):
    try:
        created_category = CategoryService.create_category(
            db,
            category,
        )

        return success_response(
            message="Category created successfully.",
            data=created_category,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=ApiResponse[
        PaginatedResponse[CategoryResponse]
    ],
)
def get_categories(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.CATEGORIES_VIEW)
    ),
):
    result = CategoryService.get_paginated(
        db,
        pagination.page,
        pagination.page_size,
    )

    return success_response(
        message="Categories retrieved successfully.",
        data=result,
    )


@router.get(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.CATEGORIES_VIEW)
    ),
):
    try:
        category = CategoryService.get_category(
            db,
            category_id,
        )

        return success_response(
            message="Category retrieved successfully.",
            data=category,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.CATEGORIES_UPDATE)
    ),
):
    try:
        updated_category = CategoryService.update_category(
            db,
            category_id,
            category,
        )

        return success_response(
            message="Category updated successfully.",
            data=updated_category,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{category_id}",
    response_model=ApiResponse[None],
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.CATEGORIES_DELETE)
    ),
):
    try:
        CategoryService.delete_category(
            db,
            category_id,
        )

        return success_response(
            message="Category deleted successfully.",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )