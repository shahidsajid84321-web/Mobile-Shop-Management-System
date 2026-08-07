from sqlalchemy.orm import Session

from app.models.stock_transaction import StockTransaction


class StockTransactionRepository:

    @staticmethod
    def create(
        db: Session,
        transaction: StockTransaction,
    ) -> StockTransaction:

        db.add(transaction)

        return transaction