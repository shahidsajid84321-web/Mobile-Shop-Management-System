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

class PurchaseReportItem(BaseModel):
    invoice_number: str
    supplier_name: str
    purchase_date: date
    total_amount: Decimal


class PurchaseReportResponse(BaseModel):
    total_purchases: Decimal
    total_invoices: int
    data: list[PurchaseReportItem]


class PaymentReportItem(BaseModel):
    invoice_number: str
    customer_name: str
    payment_date: date
    amount: Decimal
    payment_method: str
    reference_number: str | None


class PaymentReportResponse(BaseModel):
    total_payments: Decimal
    total_transactions: int
    data: list[PaymentReportItem]


class ProfitReportItem(BaseModel):
    invoice_number: str
    sale_date: date
    revenue: Decimal
    cost: Decimal
    profit: Decimal


class ProfitReportResponse(BaseModel):
    total_revenue: Decimal
    total_cost: Decimal
    total_profit: Decimal
    total_invoices: int
    data: list[ProfitReportItem] 


class StockReportItem(BaseModel):
    product_id: int
    product_name: str
    brand: str
    sku: str
    stock_quantity: int
    minimum_stock: int
    purchase_price: Decimal
    stock_value: Decimal
    stock_status: str


class StockReportResponse(BaseModel):
    total_products: int
    total_stock_quantity: int
    total_stock_value: Decimal
    low_stock_products: int
    out_of_stock_products: int
    data: list[StockReportItem]           