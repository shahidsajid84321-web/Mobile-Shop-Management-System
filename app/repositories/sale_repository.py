from sqlalchemy.orm import Session

from app.models.sale import Sale


class SaleRepository:

    @staticmethod
    def create(
        db: Session,
        sale: Sale,
    ) -> Sale:

        db.add(sale)
        db.flush()

        return sale

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(Sale)
            .order_by(Sale.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        sale_id: int,
    ):

        return (
            db.query(Sale)
            .filter(Sale.id == sale_id)
            .first()
        )

    @staticmethod
    def get_by_invoice(
        db: Session,
        invoice_number: str,
    ):

        return (
            db.query(Sale)
            .filter(
                Sale.invoice_number == invoice_number
            )
            .first()
        )