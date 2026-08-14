from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.stock_transaction import StockTransaction


class StockTransactionRepository:

    @staticmethod
    def create(
        db: Session,
        transaction: StockTransaction,
    ) -> StockTransaction:

        db.add(transaction)

        return transaction

    @staticmethod
    def get_all(
        db: Session,
        page: int,
        page_size: int,
    ):
        query = db.query(StockTransaction)
        total = query.with_entities(func.count(StockTransaction.id)).scalar() or 0
        items = (
            query.order_by(StockTransaction.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    @staticmethod
    def get_by_product(
        db: Session,
        product_id: int,
    ) -> list[StockTransaction]:

        return (
            db.query(StockTransaction)
            .filter(
                StockTransaction.product_id == product_id
            )
            .order_by(StockTransaction.id.desc())
            .all()
        )