from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.customers.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate
from app.modules.customers.customer_service import CustomerService
from app.modules.permissions.permission_dependencies import require_permission
from app.shared.common_schema import ApiResponse
from app.shared.pagination import PaginationParams, PaginatedResponse
from app.shared.responses import success_response

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=ApiResponse[CustomerResponse], status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db),
                    current_user=Depends(require_permission(PermissionCode.CUSTOMERS_CREATE))):
    return success_response("Customer created successfully.", CustomerService.create(db, customer))

@router.get("/", response_model=ApiResponse[PaginatedResponse[CustomerResponse]])
def get_customers(pagination: PaginationParams = Depends(), db: Session = Depends(get_db),
                  current_user=Depends(require_permission(PermissionCode.CUSTOMERS_VIEW))):
    return success_response("Customers retrieved successfully.",
                            CustomerService.get_all(db, pagination.page, pagination.page_size))

@router.get("/{customer_id}", response_model=ApiResponse[CustomerResponse])
def get_customer(customer_id: int, db: Session = Depends(get_db),
                 current_user=Depends(require_permission(PermissionCode.CUSTOMERS_VIEW))):
    return success_response("Customer retrieved successfully.", CustomerService.get_one(db, customer_id))

@router.put("/{customer_id}", response_model=ApiResponse[CustomerResponse])
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db),
                    current_user=Depends(require_permission(PermissionCode.CUSTOMERS_UPDATE))):
    return success_response("Customer updated successfully.",
                            CustomerService.update(db, customer_id, customer))

@router.delete("/{customer_id}", response_model=ApiResponse[None])
def delete_customer(customer_id: int, db: Session = Depends(get_db),
                    current_user=Depends(require_permission(PermissionCode.CUSTOMERS_DELETE))):
    CustomerService.delete(db, customer_id)
    return success_response("Customer deleted successfully.")
