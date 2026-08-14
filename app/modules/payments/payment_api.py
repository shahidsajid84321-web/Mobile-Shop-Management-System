from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.payments.payment_schema import PaymentCreate, PaymentResponse
from app.modules.payments.payment_service import PaymentService
from app.modules.permissions.permission_dependencies import require_permission
from app.shared.common_schema import ApiResponse
from app.shared.pagination import PaginationParams, PaginatedResponse
from app.shared.responses import success_response
from app.modules.payments.payment_event_schema import PaymentWebhookRequest
from app.modules.payments.payment_event_service import PaymentEventService

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=ApiResponse[PaymentResponse], status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db), current_user=Depends(require_permission(PermissionCode.PAYMENTS_CREATE))):
    return success_response("Payment created successfully.", PaymentService.create(db, payment))

@router.get("/", response_model=ApiResponse[PaginatedResponse[PaymentResponse]])
def get_payments(pagination: PaginationParams = Depends(), db: Session = Depends(get_db), current_user=Depends(require_permission(PermissionCode.PAYMENTS_VIEW))):
    return success_response("Payments retrieved successfully.", PaymentService.get_all(db, pagination))

@router.post("/webhooks", response_model=ApiResponse[dict])
def payment_webhook(data: PaymentWebhookRequest, db: Session = Depends(get_db), x_webhook_secret: str | None = Header(default=None, alias="X-Webhook-Secret")):
    if not settings.PAYMENT_WEBHOOK_SECRET or x_webhook_secret != settings.PAYMENT_WEBHOOK_SECRET:
        raise UnauthorizedException("Invalid payment webhook credentials.")
    event, created = PaymentEventService.process(db, data)
    return success_response("Payment webhook accepted." if created else "Payment webhook already processed.", {"event_id": event.event_id, "processed": created})

@router.get("/{payment_id}", response_model=ApiResponse[PaymentResponse])
def get_payment(payment_id: int, db: Session = Depends(get_db), current_user=Depends(require_permission(PermissionCode.PAYMENTS_VIEW))):
    return success_response("Payment retrieved successfully.", PaymentService.get_one(db, payment_id))
