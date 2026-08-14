from sqlalchemy.orm import Session

from app.models.purchase import Purchase


class PurchaseRepository:

    @staticmethod
    def create(
        db: Session,
        purchase: Purchase,
    ) -> Purchase:

        db.add(purchase)
        db.flush()

        return purchase

    @staticmethod
    def get_all(
        db: Session,
        page: int,
        page_size: int,
    ) -> tuple[list[Purchase], int]:

        query = (
            db.query(Purchase)
            .order_by(Purchase.id.desc())
        )

        total = query.count()

        offset = (page - 1) * page_size

        purchases = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return purchases, total

    @staticmethod
    def get_by_id(
        db: Session,
        purchase_id: int,
    ) -> Purchase | None:

        return (
            db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

    @staticmethod
    def get_by_invoice_number(
        db: Session,
        invoice_number: str,
    ) -> Purchase | None:

        return (
            db.query(Purchase)
            .filter(
                Purchase.invoice_number == invoice_number
            )
            .first()
        )