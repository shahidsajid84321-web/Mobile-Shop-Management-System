from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/sales")
def sales_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    return ReportService.sales_report(
        db,
        start_date,
        end_date,
    )