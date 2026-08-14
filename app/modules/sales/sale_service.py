from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.stock_transaction import StockTransaction
from app.modules.customers.customer_repository import CustomerRepository
from app.modules.inventory.inventory_repository import StockTransactionRepository
from app.modules.products.product_repository import ProductRepository
from app.modules.sales.sale_item_repository import SaleItemRepository
from app.modules.sales.sale_repository import SaleRepository
from app.modules.sales.sale_schema import SaleCreate

from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
)

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
            raise BadRequestException("Invoice number already exists.")

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

                product = ProductRepository.get_by_id_for_update(
                    db,
                    item.product_id,
                )

                if product is None:
                    raise NotFoundException(f"Product {item.product_id} not found.")

                if product.stock_quantity < item.quantity:
                    raise BadRequestException(f"Insufficient stock for {product.name}")

                subtotal = item.quantity * item.unit_price

                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    cost_price=product.purchase_price,
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

            if data.discount > total:
                raise BadRequestException(
                    "Discount cannot exceed the sale subtotal."
                )

            sale.total_amount = total
            sale.grand_total = total - data.discount + data.tax

            if sale.grand_total < Decimal("0.00"):
                raise BadRequestException(
                    "Sale grand total cannot be negative."
                )

            if sale.grand_total == Decimal("0.00"):
                sale.payment_status = "Paid"

            db.commit()

            db.refresh(sale)

            return sale

        except Exception:

            db.rollback()
            raise

    @staticmethod
    def get_all(
        db: Session,
        pagination: PaginationParams,
    ) -> PaginatedResponse[Sale]:

        page = pagination.page
        page_size = pagination.page_size

        sales, total = SaleRepository.get_all(
            db,
            page,
            page_size,
        )

        return PaginatedResponse.create(
            items=sales,
            page=page,
            page_size=page_size,
            total=total,
        )

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
            raise NotFoundException("Sale not found.")

        return sale
