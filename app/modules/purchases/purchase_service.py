from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, NotFoundException

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.stock_transaction import StockTransaction
from app.modules.inventory.inventory_repository import StockTransactionRepository
from app.modules.products.product_repository import ProductRepository
from app.modules.purchases.purchase_item_repository import PurchaseItemRepository
from app.modules.purchases.purchase_repository import PurchaseRepository
from app.modules.purchases.purchase_schema import PurchaseCreate
from app.modules.suppliers.supplier_repository import SupplierRepository

from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
)


class PurchaseService:

    @staticmethod
    def create(
        db: Session,
        data: PurchaseCreate,
    ) -> Purchase:

        supplier = SupplierRepository.get_by_id(
            db,
            data.supplier_id,
        )

        if supplier is None:
            raise NotFoundException("Supplier not found.")

        existing = PurchaseRepository.get_by_invoice_number(
            db,
            data.invoice_number,
        )

        if existing:
            raise BadRequestException("Invoice number already exists.")

        purchase = Purchase(
            supplier_id=data.supplier_id,
            invoice_number=data.invoice_number,
            purchase_date=data.purchase_date,
            total_amount=Decimal("0.00"),
            remarks=data.remarks,
        )

        try:

            PurchaseRepository.create(
                db,
                purchase,
            )

            total = Decimal("0.00")

            for item in data.items:

                product = ProductRepository.get_by_id_for_update(
                    db,
                    item.product_id,
                )

                if product is None:
                    raise NotFoundException(f"Product {item.product_id} not found.")

                subtotal = item.quantity * item.unit_price

                purchase_item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=subtotal,
                )

                PurchaseItemRepository.create(
                    db,
                    purchase_item,
                )

                previous_quantity = product.stock_quantity
                previous_cost = product.purchase_price
                new_quantity = previous_quantity + item.quantity

                if new_quantity > 0:
                    weighted_cost = (
                        (previous_quantity * previous_cost)
                        + (item.quantity * item.unit_price)
                    ) / new_quantity
                    product.purchase_price = weighted_cost.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )

                product.stock_quantity = new_quantity

                stock = StockTransaction(
                    product_id=product.id,
                    transaction_type="IN",
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    remarks=f"Purchase {purchase.invoice_number}",
                )

                StockTransactionRepository.create(
                    db,
                    stock,
                )

                total += subtotal

            purchase.total_amount = total

            db.commit()

            db.refresh(purchase)

            return purchase

        except Exception:

            db.rollback()

            raise

    @staticmethod
    def get_all(
        db: Session,
        pagination: PaginationParams,
    ) -> PaginatedResponse[Purchase]:

        page = pagination.page
        page_size = pagination.page_size

        purchases, total = PurchaseRepository.get_all(
            db,
            page,
            page_size,
        )

        return PaginatedResponse.create(
            items=purchases,
            page=page,
            page_size=page_size,
            total=total,
        )

    @staticmethod
    def get_one(
        db: Session,
        purchase_id: int,
    ):

        purchase = PurchaseRepository.get_by_id(
            db,
            purchase_id,
        )

        if purchase is None:
            raise NotFoundException("Purchase not found.")

        return purchase
