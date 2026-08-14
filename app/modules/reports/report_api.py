from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.permissions.permission_dependencies import require_permission

from app.modules.reports.report_schema import (
    SalesReportResponse,
    PurchaseReportResponse,
    PaymentReportResponse,
    ProfitReportResponse,
    StockReportResponse,
)

from app.modules.reports.report_service import ReportService
from app.shared.common_schema import ApiResponse
from app.shared.responses import success_response


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/sales",
    response_model=ApiResponse[SalesReportResponse],
)
def sales_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.REPORTS_VIEW)
    ),
):

    try:

        return success_response("Sales report generated successfully.", ReportService.sales_report(db, start_date, end_date))

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/purchases",
    response_model=ApiResponse[PurchaseReportResponse],
)
def purchase_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.REPORTS_VIEW)
    ),
):

    try:

        return success_response("Purchase report generated successfully.", ReportService.purchase_report(db, start_date, end_date))

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/payments",
    response_model=ApiResponse[PaymentReportResponse],
)
def payment_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.REPORTS_VIEW)
    ),
):

    try:

        return success_response("Payment report generated successfully.", ReportService.payment_report(db, start_date, end_date))

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) 


@router.get(
    "/profit",
    response_model=ApiResponse[ProfitReportResponse],
)
def profit_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.REPORTS_VIEW)
    ),
):

    try:

        return success_response("Profit report generated successfully.", ReportService.profit_report(db, start_date, end_date))

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )



@router.get(
    "/stock",
    response_model=ApiResponse[StockReportResponse],
)
def stock_report(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PermissionCode.REPORTS_VIEW)
    ),
):
    return success_response("Stock report generated successfully.", ReportService.stock_report(db))           