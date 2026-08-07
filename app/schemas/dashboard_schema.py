from decimal import Decimal

from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_products: int
    total_categories: int
    total_customers: int
    total_suppliers: int

    total_sales: Decimal
    total_purchases: Decimal

    today_sales: Decimal
    today_purchases: Decimal

    pending_payments: Decimal

    low_stock_products: int

    profit: Decimal