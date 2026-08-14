from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import require_permission
from app.modules.sales.sale_schema import SaleCreate, SaleResponse
from app.modules.sales.sale_service import SaleService
from app.shared.common_schema import ApiResponse
from app.shared.pagination import PaginationParams, PaginatedResponse
from app.shared.responses import success_response

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=ApiResponse[SaleResponse], status_code=status.HTTP_201_CREATED)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db),
                current_user=Depends(require_permission(PermissionCode.SALES_CREATE))):
    return success_response("Sale created successfully.", SaleService.create(db, sale))

@router.get("/", response_model=ApiResponse[PaginatedResponse[SaleResponse]])
def get_sales(pagination: PaginationParams = Depends(), db: Session = Depends(get_db),
              current_user=Depends(require_permission(PermissionCode.SALES_VIEW))):
    return success_response("Sales retrieved successfully.", SaleService.get_all(db, pagination))

@router.get("/{sale_id}", response_model=ApiResponse[SaleResponse])
def get_sale(sale_id: int, db: Session = Depends(get_db),
             current_user=Depends(require_permission(PermissionCode.SALES_VIEW))):
    return success_response("Sale retrieved successfully.", SaleService.get_one(db, sale_id))
