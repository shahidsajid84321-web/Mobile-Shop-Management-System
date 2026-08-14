from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.inventory.inventory_schema import StockTransactionCreate, StockTransactionResponse
from app.modules.inventory.inventory_service import StockTransactionService
from app.modules.permissions.permission_dependencies import require_permission
from app.shared.common_schema import ApiResponse
from app.shared.pagination import PaginationParams, PaginatedResponse
from app.shared.responses import success_response

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=ApiResponse[StockTransactionResponse], status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: StockTransactionCreate, db: Session = Depends(get_db),
                       current_user=Depends(require_permission(PermissionCode.INVENTORY_ADJUST))):
    return success_response("Inventory transaction created successfully.",
                            StockTransactionService.create(db, transaction))

@router.get("/", response_model=ApiResponse[PaginatedResponse[StockTransactionResponse]])
def get_transactions(pagination: PaginationParams = Depends(), db: Session = Depends(get_db),
                     current_user=Depends(require_permission(PermissionCode.INVENTORY_VIEW))):
    return success_response("Inventory transactions retrieved successfully.",
                            StockTransactionService.get_all(db, pagination))

@router.get("/product/{product_id}", response_model=ApiResponse[PaginatedResponse[StockTransactionResponse]])
def get_product_transactions(product_id: int, pagination: PaginationParams = Depends(),
                             db: Session = Depends(get_db),
                             current_user=Depends(require_permission(PermissionCode.INVENTORY_VIEW))):
    return success_response("Product inventory transactions retrieved successfully.",
                            StockTransactionService.get_by_product(db, product_id, pagination))
