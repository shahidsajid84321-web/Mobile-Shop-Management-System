from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db

from app.schemas.common_schema import ApiResponse

from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):
    customer = CustomerService.create(
        db,
        customer,
    )

    return ApiResponse(
        success=True,
        message="Customer created successfully.",
        data=customer,
    )


@router.get(
    "/",
    response_model=list[CustomerResponse],
)
def get_customers(
    db: Session = Depends(get_db),
):
    customers = CustomerService.get_all(db)

    return ApiResponse(
        success=True,
        message="Customers retrieved successfully.",
        data=customers,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = CustomerService.get_one(
        db,
        customer_id,
    )

    return ApiResponse(
        success=True,
        message="Customer retrieved successfully.",
        data=customer,
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
):
    try:
        return CustomerService.update(
            db,
            customer_id,
            customer,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{customer_id}",
    status_code=204,
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    try:
        CustomerService.delete(
            db,
            customer_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )