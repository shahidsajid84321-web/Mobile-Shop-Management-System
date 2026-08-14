from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import require_permission
from app.modules.suppliers.supplier_schema import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from app.modules.suppliers.supplier_service import SupplierService

from app.shared.common_schema import ApiResponse
from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
)
from app.shared.responses import success_response


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post(
    "/",
    response_model=ApiResponse[SupplierResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.SUPPLIERS_CREATE)
    ),
):
    try:
        return success_response(
            message="Supplier created successfully.",
            data=SupplierService.create(
                db,
                supplier,
            ),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=ApiResponse[
        PaginatedResponse[SupplierResponse]
    ],
)
def get_suppliers(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.SUPPLIERS_VIEW)
    ),
):
    data = SupplierService.get_all(
        db,
        pagination,
    )

    return success_response(
        message="Suppliers retrieved successfully.",
        data=data,
    )


@router.get(
    "/{supplier_id}",
    response_model=ApiResponse[SupplierResponse],
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.SUPPLIERS_VIEW)
    ),
):
    try:
        supplier = SupplierService.get_one(
            db,
            supplier_id,
        )

        return success_response(
            message="Supplier retrieved successfully.",
            data=supplier,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{supplier_id}",
    response_model=ApiResponse[SupplierResponse],
)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.SUPPLIERS_UPDATE)
    ),
):
    try:
        updated_supplier = SupplierService.update(
            db,
            supplier_id,
            supplier,
        )

        return success_response(
            message="Supplier updated successfully.",
            data=updated_supplier,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{supplier_id}",
    response_model=ApiResponse[None],
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.SUPPLIERS_DELETE)
    ),
):
    try:
        SupplierService.delete(
            db,
            supplier_id,
        )

        return success_response(
            message="Supplier deleted successfully.",
            data=None,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )