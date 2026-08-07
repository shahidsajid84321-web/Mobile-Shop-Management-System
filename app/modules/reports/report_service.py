from datetime import date

from sqlalchemy.orm import Session

from app.modules.reports.report_repository import ReportRepository


class ReportService:

    @staticmethod
    def sales_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):
        return ReportRepository.sales_report(
            db,
            start_date,
            end_date,
        )
