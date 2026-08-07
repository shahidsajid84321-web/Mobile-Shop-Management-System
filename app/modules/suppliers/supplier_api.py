from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.modules.suppliers.supplier_schema import (SupplierCreate,
                                                   SupplierResponse,
                                                   SupplierUpdate)
from app.modules.suppliers.supplier_service import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=201,
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
):
    try:
        return SupplierService.create(
            db,
            supplier,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[SupplierResponse],
)
def get_suppliers(
    db: Session = Depends(get_db),
):
    return SupplierService.get_all(db)


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    try:
        return SupplierService.get_one(
            db,
            supplier_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse,
)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
):
    try:
        return SupplierService.update(
            db,
            supplier_id,
            supplier,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{supplier_id}",
    status_code=204,
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    try:
        SupplierService.delete(
            db,
            supplier_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
