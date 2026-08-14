from datetime import date

from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException

from app.modules.reports.report_repository import ReportRepository


class ReportService:

    @staticmethod
    def sales_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):

        if start_date > end_date:
            raise BadRequestException(
                "start_date cannot be after end_date."
            )

        return ReportRepository.sales_report(
            db,
            start_date,
            end_date,
        )


    @staticmethod
    def purchase_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):

        if start_date > end_date:
            raise BadRequestException(
                "start_date cannot be after end_date."
            )

        return ReportRepository.purchase_report(
            db,
            start_date,
            end_date,
        )    


    @staticmethod
    def payment_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):

        if start_date > end_date:
            raise BadRequestException(
                "start_date cannot be after end_date."
            )

        return ReportRepository.payment_report(
            db,
            start_date,
            end_date,
        )


    @staticmethod
    def profit_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):

        if start_date > end_date:
            raise BadRequestException(
                "start_date cannot be after end_date."
            )

        return ReportRepository.profit_report(
            db,
            start_date,
            end_date,
        )


    @staticmethod
    def stock_report(
        db: Session,
    ):
        return ReportRepository.stock_report(db)    
        