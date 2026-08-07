from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.stock_transaction import StockTransaction
from app.modules.customers.customer_repository import CustomerRepository
from app.modules.inventory.inventory_repository import \
    StockTransactionRepository
from app.modules.products.product_repository import ProductRepository
from app.modules.sales.sale_item_repository import SaleItemRepository
from app.modules.sales.sale_repository import SaleRepository
from app.modules.sales.sale_schema import SaleCreate


class SaleService:

    @staticmethod
    def create(
        db: Session,
        data: SaleCreate,
    ) -> Sale:

        customer = CustomerRepository.get_by_id(
            db,
            data.customer_id,
        )

        if customer is None:
            raise NotFoundException("Customer not found.")

        existing = SaleRepository.get_by_invoice(
            db,
            data.invoice_number,
        )

        if existing:
            raise ValueError("Invoice number already exists.")

        sale = Sale(
            customer_id=data.customer_id,
            invoice_number=data.invoice_number,
            sale_date=data.sale_date,
            total_amount=Decimal("0.00"),
            discount=data.discount,
            tax=data.tax,
            grand_total=Decimal("0.00"),
            payment_status="Pending",
            remarks=data.remarks,
        )

        try:

            SaleRepository.create(
                db,
                sale,
            )

            total = Decimal("0.00")

            for item in data.items:

                product = ProductRepository.get_by_id(
                    db,
                    item.product_id,
                )

                if product is None:
                    raise ValueError(f"Product {item.product_id} not found.")

                if product.stock_quantity < item.quantity:
                    raise ValueError(f"Insufficient stock for {product.name}")

                subtotal = item.quantity * item.unit_price

                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=subtotal,
                )

                SaleItemRepository.create(
                    db,
                    sale_item,
                )

                product.stock_quantity -= item.quantity

                stock = StockTransaction(
                    product_id=product.id,
                    transaction_type="OUT",
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    remarks=f"Sale {sale.invoice_number}",
                )

                StockTransactionRepository.create(
                    db,
                    stock,
                )

                total += subtotal

            sale.total_amount = total
            sale.grand_total = total - data.discount + data.tax

            db.commit()

            db.refresh(sale)

            return sale

        except Exception:

            db.rollback()
            raise

    @staticmethod
    def get_all(
        db: Session,
    ):
        return SaleRepository.get_all(db)

    @staticmethod
    def get_one(
        db: Session,
        sale_id: int,
    ):

        sale = SaleRepository.get_by_id(
            db,
            sale_id,
        )

        if sale is None:
            raise ValueError("Sale not found.")

        return sale
