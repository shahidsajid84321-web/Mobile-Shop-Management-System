from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import require_permission
from app.modules.purchases.purchase_schema import PurchaseCreate, PurchaseResponse
from app.modules.purchases.purchase_service import PurchaseService
from app.shared.common_schema import ApiResponse
from app.shared.pagination import PaginationParams, PaginatedResponse
from app.shared.responses import success_response

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/", response_model=ApiResponse[PurchaseResponse], status_code=status.HTTP_201_CREATED)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db),
                    current_user=Depends(require_permission(PermissionCode.PURCHASES_CREATE))):
    return success_response("Purchase created successfully.", PurchaseService.create(db, purchase))

@router.get("/", response_model=ApiResponse[PaginatedResponse[PurchaseResponse]])
def get_purchases(pagination: PaginationParams = Depends(), db: Session = Depends(get_db),
                  current_user=Depends(require_permission(PermissionCode.PURCHASES_VIEW))):
    return success_response("Purchases retrieved successfully.", PurchaseService.get_all(db, pagination))

@router.get("/{purchase_id}", response_model=ApiResponse[PurchaseResponse])
def get_purchase(purchase_id: int, db: Session = Depends(get_db),
                 current_user=Depends(require_permission(PermissionCode.PURCHASES_VIEW))):
    return success_response("Purchase retrieved successfully.", PurchaseService.get_one(db, purchase_id))
