from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.product import Product
from app.models.purchase import Purchase
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
                Sale.is_voided.is_(False),
            )
            .order_by(Sale.sale_date.desc(), Sale.id.desc())
            .all()
        )

        total_sales = sum(
            (sale.grand_total for sale in sales),
            Decimal("0.00"),
        )

        data = []
        for sale in sales:
            customer_name = (
                sale.customer.full_name
                if sale.customer
                else "Unknown"
            )

            data.append(
                {
                    "invoice_number": sale.invoice_number,
                    "customer_name": customer_name,
                    "sale_date": sale.sale_date,
                    "grand_total": sale.grand_total,
                    "payment_status": sale.payment_status,
                }
            )

        return {
            "total_sales": total_sales,
            "total_invoices": len(sales),
            "data": data,
        }

    @staticmethod
    def purchase_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):
        purchases = (
            db.query(Purchase)
            .filter(
                Purchase.purchase_date >= start_date,
                Purchase.purchase_date <= end_date,
            )
            .order_by(
                Purchase.purchase_date.desc(),
                Purchase.id.desc(),
            )
            .all()
        )

        total_purchases = sum(
            (purchase.total_amount for purchase in purchases),
            Decimal("0.00"),
        )

        data = []
        for purchase in purchases:
            supplier_name = (
                purchase.supplier.company_name
                if purchase.supplier
                else "Unknown"
            )

            data.append(
                {
                    "invoice_number": purchase.invoice_number,
                    "supplier_name": supplier_name,
                    "purchase_date": purchase.purchase_date,
                    "total_amount": purchase.total_amount,
                }
            )

        return {
            "total_purchases": total_purchases,
            "total_invoices": len(purchases),
            "data": data,
        }

    @staticmethod
    def payment_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):
        payments = (
            db.query(Payment)
            .filter(
                Payment.payment_date >= start_date,
                Payment.payment_date <= end_date,
            )
            .order_by(
                Payment.payment_date.desc(),
                Payment.id.desc(),
            )
            .all()
        )

        total_payments = sum(
            (payment.amount for payment in payments),
            Decimal("0.00"),
        )

        data = []
        for payment in payments:
            sale = payment.sale

            customer_name = (
                sale.customer.full_name
                if sale and sale.customer
                else "Unknown"
            )

            invoice_number = (
                sale.invoice_number
                if sale
                else "Unknown"
            )

            data.append(
                {
                    "invoice_number": invoice_number,
                    "customer_name": customer_name,
                    "payment_date": payment.payment_date,
                    "amount": payment.amount,
                    "payment_method": payment.payment_method,
                    "reference_number": payment.reference_number,
                }
            )

        return {
            "total_payments": total_payments,
            "total_transactions": len(payments),
            "data": data,
        }

    @staticmethod
    def profit_report(
        db: Session,
        start_date: date,
        end_date: date,
    ):
        sales = (
            db.query(Sale)
            .filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date,
                Sale.is_voided.is_(False),
            )
            .order_by(
                Sale.sale_date.desc(),
                Sale.id.desc(),
            )
            .all()
        )

        total_revenue = Decimal("0.00")
        total_cost = Decimal("0.00")
        data = []

        for sale in sales:
            revenue = sale.total_amount - sale.discount
            cost = Decimal("0.00")

            for item in sale.items:
                cost += item.cost_price * item.quantity

            profit = revenue - cost
            total_revenue += revenue
            total_cost += cost

            data.append(
                {
                    "invoice_number": sale.invoice_number,
                    "sale_date": sale.sale_date,
                    "revenue": revenue,
                    "cost": cost,
                    "profit": profit,
                }
            )

        return {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "total_profit": total_revenue - total_cost,
            "total_invoices": len(sales),
            "data": data,
        }

    @staticmethod
    def stock_report(
        db: Session,
    ):
        products = (
            db.query(Product)
            .filter(Product.is_active.is_(True))
            .order_by(Product.name.asc())
            .all()
        )

        total_stock_quantity = 0
        total_stock_value = Decimal("0.00")
        low_stock_products = 0
        out_of_stock_products = 0
        data = []

        for product in products:
            stock_value = product.stock_quantity * product.purchase_price

            if product.stock_quantity == 0:
                stock_status = "Out of Stock"
                out_of_stock_products += 1
            elif product.stock_quantity <= product.minimum_stock:
                stock_status = "Low Stock"
                low_stock_products += 1
            else:
                stock_status = "In Stock"

            total_stock_quantity += product.stock_quantity
            total_stock_value += stock_value

            data.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "brand": product.brand,
                    "sku": product.sku,
                    "stock_quantity": product.stock_quantity,
                    "minimum_stock": product.minimum_stock,
                    "purchase_price": product.purchase_price,
                    "stock_value": stock_value,
                    "stock_status": stock_status,
                }
            )

        return {
            "total_products": len(products),
            "total_stock_quantity": total_stock_quantity,
            "total_stock_value": total_stock_value,
            "low_stock_products": low_stock_products,
            "out_of_stock_products": out_of_stock_products,
            "data": data,
        }
