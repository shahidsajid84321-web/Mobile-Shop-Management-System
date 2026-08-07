from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.sale import Sale


class ReportRepository:

    @staticmethod
    def sales_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):

        sales = (
            db.query(Sale)
            .filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date,
            )
            .all()
        )

        total_sales = sum(sale.grand_total for sale in sales)

        return {
            "total_sales": total_sales,
            "total_invoices": len(sales),
            "data": sales,
        }
