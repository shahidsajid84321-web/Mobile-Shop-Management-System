from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, NotFoundException

from app.models.product import Product
from app.models.stock_transaction import StockTransaction
from app.modules.inventory.inventory_repository import StockTransactionRepository
from app.modules.inventory.inventory_schema import StockTransactionCreate, StockTransactionResponse
from app.shared.pagination import PaginationParams, PaginatedResponse


class StockTransactionService:

    @staticmethod
    def create(
        db: Session,
        data: StockTransactionCreate,
    ) -> StockTransaction:

        product = db.query(Product).filter(Product.id == data.product_id).with_for_update().first()

        if product is None:
            raise NotFoundException("Product not found.")

        if data.transaction_type == "IN":
            previous_quantity = product.stock_quantity
            previous_cost = product.purchase_price
            new_quantity = previous_quantity + data.quantity

            if new_quantity > 0:
                weighted_cost = (
                    (previous_quantity * previous_cost)
                    + (data.quantity * data.unit_price)
                ) / new_quantity
                product.purchase_price = weighted_cost.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )

            product.stock_quantity = new_quantity

        elif data.transaction_type == "OUT":

            if product.stock_quantity < data.quantity:
                raise BadRequestException("Insufficient stock.")

            product.stock_quantity -= data.quantity

        else:
            raise BadRequestException("transaction_type must be IN or OUT.")

        transaction = StockTransaction(
            product_id=data.product_id,
            transaction_type=data.transaction_type,
            quantity=data.quantity,
            unit_price=data.unit_price,
            remarks=data.remarks,
        )

        try:
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            return transaction
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(
        db: Session,
        pagination: PaginationParams,
    ) -> PaginatedResponse[StockTransactionResponse]:
        items, total = StockTransactionRepository.get_all(
            db, pagination.page, pagination.page_size
        )
        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        )

    @staticmethod
    def get_by_product(
        db: Session,
        product_id: int,
        pagination: PaginationParams,
    ) -> PaginatedResponse[StockTransactionResponse]:
        items, total = StockTransactionRepository.get_by_product(
            db, product_id, pagination.page, pagination.page_size
        )
        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        )
