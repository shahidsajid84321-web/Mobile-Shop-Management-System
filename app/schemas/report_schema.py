from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SalesReportItem(BaseModel):
    invoice_number: str
    customer_name: str
    sale_date: date
    grand_total: Decimal
    payment_status: str


class SalesReportResponse(BaseModel):
    total_sales: Decimal
    total_invoices: int
    data: list[SalesReportItem]