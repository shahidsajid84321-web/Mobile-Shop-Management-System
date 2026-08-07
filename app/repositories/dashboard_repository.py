from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.categories.category_model import Category
from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.supplier import Supplier


class DashboardRepository:

    @staticmethod
    def get_statistics(
        db: Session,
    ):

        today = date.today()

        return {

            "total_products":
                db.query(Product).count(),

            "total_categories":
                db.query(Category).count(),

            "total_customers":
                db.query(Customer).count(),

            "total_suppliers":
                db.query(Supplier).count(),

            "total_sales":
                db.query(
                    func.coalesce(
                        func.sum(Sale.grand_total),
                        Decimal("0.00"),
                    )
                ).scalar(),

            "total_purchases":
                db.query(
                    func.coalesce(
                        func.sum(Purchase.grand_total),
                        Decimal("0.00"),
                    )
                ).scalar(),

            "today_sales":
                db.query(
                    func.coalesce(
                        func.sum(Sale.grand_total),
                        Decimal("0.00"),
                    )
                ).filter(
                    Sale.sale_date == today,
                ).scalar(),

            "today_purchases":
                db.query(
                    func.coalesce(
                        func.sum(Purchase.grand_total),
                        Decimal("0.00"),
                    )
                ).filter(
                    Purchase.purchase_date == today,
                ).scalar(),

            "pending_payments":
                db.query(
                    func.coalesce(
                        func.sum(
                            Sale.grand_total
                        ),
                        Decimal("0.00"),
                    )
                ).filter(
                    Sale.payment_status != "Paid",
                ).scalar(),

            "low_stock_products":
                db.query(Product)
                .filter(
                    Product.stock_quantity <= 5
                )
                .count(),

            "profit":
                (
                    db.query(
                        func.coalesce(
                            func.sum(
                                Sale.grand_total
                            ),
                            Decimal("0.00"),
                        )
                    ).scalar()
                    -
                    db.query(
                        func.coalesce(
                            func.sum(
                                Purchase.grand_total
                            ),
                            Decimal("0.00"),
                        )
                    ).scalar()
                )
        }