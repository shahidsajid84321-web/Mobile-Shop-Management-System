from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import require_permission
from app.modules.products.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.modules.products.product_service import ProductService

from app.shared.common_schema import ApiResponse
from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
)
from app.shared.responses import success_response


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.PRODUCTS_CREATE)
    ),
):
    try:
        created_product = ProductService.create_product(
            db,
            product,
        )

        return success_response(
            message="Product created successfully.",
            data=created_product,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=ApiResponse[
        PaginatedResponse[ProductResponse]
    ],
)
def get_products(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.PRODUCTS_VIEW)
    ),
):
    result = ProductService.get_paginated(
        db,
        pagination.page,
        pagination.page_size,
    )

    return success_response(
        message="Products retrieved successfully.",
        data=result,
    )


@router.get(
    "/{product_id}",
    response_model=ApiResponse[ProductResponse],
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.PRODUCTS_VIEW)
    ),
):
    try:
        found_product = ProductService.get_product(
            db,
            product_id,
        )

        return success_response(
            message="Product retrieved successfully.",
            data=found_product,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{product_id}",
    response_model=ApiResponse[ProductResponse],
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.PRODUCTS_UPDATE)
    ),
):
    try:
        updated_product = ProductService.update_product(
            db,
            product_id,
            product,
        )

        return success_response(
            message="Product updated successfully.",
            data=updated_product,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{product_id}",
    response_model=ApiResponse[None],
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.PRODUCTS_DELETE)
    ),
):
    try:
        ProductService.delete_product(
            db,
            product_id,
        )

        return success_response(
            message="Product deleted successfully.",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )