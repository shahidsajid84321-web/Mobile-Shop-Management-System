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
    ) -> list[Purchase]:

        return db.query(Purchase).order_by(Purchase.id.desc()).all()

    @staticmethod
    def get_by_id(
        db: Session,
        purchase_id: int,
    ) -> Purchase | None:

        return db.query(Purchase).filter(Purchase.id == purchase_id).first()
