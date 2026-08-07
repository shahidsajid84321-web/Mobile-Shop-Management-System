from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_transaction import StockTransaction

from app.repositories.stock_transaction_repository import (
    StockTransactionRepository,
)

from app.schemas.stock_transaction_schema import (
    StockTransactionCreate,
)


class StockTransactionService:

    @staticmethod
    def create(
        db: Session,
        data: StockTransactionCreate,
    ) -> StockTransaction:

        product = (
            db.query(Product)
            .filter(Product.id == data.product_id)
            .first()
        )

        if product is None:
            raise ValueError("Product not found.")

        if data.transaction_type == "IN":
            product.stock_quantity += data.quantity

        elif data.transaction_type == "OUT":

            if product.stock_quantity < data.quantity:
                raise ValueError("Insufficient stock.")

            product.stock_quantity -= data.quantity

        else:
            raise ValueError(
                "transaction_type must be IN or OUT."
            )

        transaction = StockTransaction(
            product_id=data.product_id,
            transaction_type=data.transaction_type,
            quantity=data.quantity,
            unit_price=data.unit_price,
            remarks=data.remarks,
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_all(
        db: Session,
    ):
        return StockTransactionRepository.get_all(db)

    @staticmethod
    def get_by_product(
        db: Session,
        product_id: int,
    ):
        return StockTransactionRepository.get_by_product(
            db,
            product_id,
        )