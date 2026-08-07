from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.stock_transaction import StockTransaction

from app.repositories.product_repository import ProductRepository
from app.repositories.purchase_item_repository import PurchaseItemRepository
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.stock_transaction_repository import (
    StockTransactionRepository,
)
from app.repositories.supplier_repository import SupplierRepository

from app.schemas.purchase_schema import PurchaseCreate


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
            raise ValueError("Supplier not found.")

        existing = (
            db.query(Purchase)
            .filter(
                Purchase.invoice_number == data.invoice_number
            )
            .first()
        )

        if existing:
            raise ValueError(
                "Invoice number already exists."
            )

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

                product = ProductRepository.get_by_id(
                    db,
                    item.product_id,
                )

                if product is None:
                    raise ValueError(
                        f"Product {item.product_id} not found."
                    )

                subtotal = (
                    item.quantity
                    * item.unit_price
                )

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

                product.stock_quantity += item.quantity

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
    ):
        return PurchaseRepository.get_all(db)

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
            raise ValueError(
                "Purchase not found."
            )

        return purchase