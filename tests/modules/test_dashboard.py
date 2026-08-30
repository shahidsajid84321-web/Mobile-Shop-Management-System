from decimal import Decimal
from app.modules.dashboard.dashboard_schema import DashboardResponse

def test_dashboard_response_accepts_numeric_totals():
    data = {k: 0 for k in ["total_products","active_products","low_stock_products","out_of_stock_products","total_categories","total_customers","total_suppliers","total_sales_count","total_purchases_count","total_stock","total_stock_in","total_stock_out"]}
    for k in ["total_sales_amount","today_sales_amount","total_purchases_amount","today_purchases_amount","total_paid_amount","pending_payments","gross_profit"]: data[k] = Decimal("0")
    result = DashboardResponse(**data)
    assert result.total_products == 0 and result.gross_profit == Decimal("0")
