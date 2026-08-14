from decimal import Decimal

from pydantic import BaseModel


class DashboardResponse(BaseModel):

    # -------------------------
    # Basic Counts
    # -------------------------

    total_products: int
    active_products: int
    low_stock_products: int
    out_of_stock_products: int

    total_categories: int
    total_customers: int
    total_suppliers: int

    # -------------------------
    # Sales
    # -------------------------

    total_sales_count: int
    total_sales_amount: Decimal
    today_sales_amount: Decimal

    # -------------------------
    # Purchases
    # -------------------------

    total_purchases_count: int
    total_purchases_amount: Decimal
    today_purchases_amount: Decimal

    # -------------------------
    # Inventory
    # -------------------------

    total_stock: int
    total_stock_in: int
    total_stock_out: int

    # -------------------------
    # Payments
    # -------------------------

    total_paid_amount: Decimal
    pending_payments: Decimal

    # -------------------------
    # Profit
    # -------------------------

    gross_profit: Decimal