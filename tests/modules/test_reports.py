from decimal import Decimal
from app.modules.reports.report_schema import (
    SalesReportResponse, PurchaseReportResponse, PaymentReportResponse,
    ProfitReportResponse, StockReportResponse,
)

def test_empty_reports_are_valid():
    assert SalesReportResponse(total_sales=0, total_invoices=0, data=[]).data == []
    assert PurchaseReportResponse(total_purchases=0, total_invoices=0, data=[]).data == []
    assert PaymentReportResponse(total_payments=0, total_transactions=0, data=[]).data == []
    assert ProfitReportResponse(total_revenue=0, total_cost=0, total_profit=0, total_invoices=0, data=[]).total_profit == Decimal("0")
    assert StockReportResponse(total_products=0, total_stock_quantity=0, total_stock_value=0, low_stock_products=0, out_of_stock_products=0, data=[]).total_products == 0
