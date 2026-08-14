from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def create(
        db: Session,
        payment: Payment,
    ) -> Payment:

        db.add(payment)
        db.flush()

        return payment

    @staticmethod
    def get_all(
        db: Session,
        page: int,
        page_size: int,
    ):
        query = db.query(Payment)
        total = query.with_entities(func.count(Payment.id)).scalar() or 0
        items = (
            query.order_by(Payment.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    @staticmethod
    def get_by_id(
        db: Session,
        payment_id: int,
    ):

        return db.query(Payment).filter(Payment.id == payment_id).first()
