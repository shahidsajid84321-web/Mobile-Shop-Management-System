from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.payment import Payment
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.stock_transaction import StockTransaction
from app.models.supplier import Supplier
from app.modules.categories.category_model import Category


class DashboardRepository:

    @staticmethod
    def get_statistics(
        db: Session,
    ):

        today = date.today()

        # -------------------------
        # Basic Counts
        # -------------------------

        total_products = (
            db.query(Product)
            .count()
        )

        active_products = (
            db.query(Product)
            .filter(
                Product.is_active.is_(True)
            )
            .count()
        )

        low_stock_products = (
            db.query(Product)
            .filter(
                Product.stock_quantity
                <= Product.minimum_stock,
                Product.stock_quantity > 0,
            )
            .count()
        )

        out_of_stock_products = (
            db.query(Product)
            .filter(
                Product.stock_quantity <= 0
            )
            .count()
        )

        total_categories = (
            db.query(Category)
            .count()
        )

        total_customers = (
            db.query(Customer)
            .count()
        )

        total_suppliers = (
            db.query(Supplier)
            .count()
        )

        # -------------------------
        # Sales
        # -------------------------

        total_sales_count = (
            db.query(Sale)
            .filter(Sale.is_voided.is_(False))
            .count()
        )

        total_sales_amount = (
            db.query(
                func.coalesce(
                    func.sum(Sale.grand_total),
                    Decimal("0.00"),
                )
            )
            .filter(Sale.is_voided.is_(False))
            .scalar()
        )

        today_sales_amount = (
            db.query(
                func.coalesce(
                    func.sum(Sale.grand_total),
                    Decimal("0.00"),
                )
            )
            .filter(
                Sale.sale_date == today,
                Sale.is_voided.is_(False),
            )
            .scalar()
        )

        # -------------------------
        # Purchases
        # -------------------------

        total_purchases_count = (
            db.query(Purchase)
            .count()
        )

        total_purchases_amount = (
            db.query(
                func.coalesce(
                    func.sum(Purchase.total_amount),
                    Decimal("0.00"),
                )
            )
            .scalar()
        )

        today_purchases_amount = (
            db.query(
                func.coalesce(
                    func.sum(Purchase.total_amount),
                    Decimal("0.00"),
                )
            )
            .filter(
                Purchase.purchase_date == today,
            )
            .scalar()
        )

        # -------------------------
        # Inventory
        # -------------------------

        total_stock = (
            db.query(
                func.coalesce(
                    func.sum(Product.stock_quantity),
                    0,
                )
            )
            .scalar()
        )

        total_stock_in = (
            db.query(
                func.coalesce(
                    func.sum(
                        StockTransaction.quantity
                    ),
                    0,
                )
            )
            .filter(
                StockTransaction.transaction_type == "IN"
            )
            .scalar()
        )

        total_stock_out = (
            db.query(
                func.coalesce(
                    func.sum(
                        StockTransaction.quantity
                    ),
                    0,
                )
            )
            .filter(
                StockTransaction.transaction_type == "OUT"
            )
            .scalar()
        )

        # -------------------------
        # Payments
        # -------------------------

        total_paid_amount = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    Decimal("0.00"),
                )
            )
            .scalar()
        )

        total_sale_amount = (
            db.query(
                func.coalesce(
                    func.sum(Sale.grand_total),
                    Decimal("0.00"),
                )
            )
            .filter(Sale.is_voided.is_(False))
            .scalar()
        )

        pending_payments = (
            total_sale_amount
            - total_paid_amount
        )

        if pending_payments < Decimal("0.00"):
            pending_payments = Decimal("0.00")

        # -------------------------
        # Gross Profit
        # -------------------------

        gross_margin = (
            db.query(
                func.coalesce(
                    func.sum(
                        SaleItem.subtotal
                        - (SaleItem.quantity * SaleItem.cost_price)
                    ),
                    Decimal("0.00"),
                )
            )
            .scalar()
        )

        total_sales_discounts = (
            db.query(
                func.coalesce(
                    func.sum(Sale.discount),
                    Decimal("0.00"),
                )
            )
            .scalar()
        )

        gross_profit = gross_margin - total_sales_discounts

        # -------------------------
        # Final Response
        # -------------------------

        return {
            "total_products": total_products,
            "active_products": active_products,
            "low_stock_products": low_stock_products,
            "out_of_stock_products": out_of_stock_products,

            "total_categories": total_categories,
            "total_customers": total_customers,
            "total_suppliers": total_suppliers,

            "total_sales_count": total_sales_count,
            "total_sales_amount": total_sales_amount,
            "today_sales_amount": today_sales_amount,

            "total_purchases_count": total_purchases_count,
            "total_purchases_amount": total_purchases_amount,
            "today_purchases_amount": today_purchases_amount,

            "total_stock": total_stock,
            "total_stock_in": total_stock_in,
            "total_stock_out": total_stock_out,

            "total_paid_amount": total_paid_amount,
            "pending_payments": pending_payments,

            "gross_profit": gross_profit,
        }