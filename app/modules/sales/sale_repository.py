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
        page: int,
        page_size: int,
    ) -> tuple[list[Sale], int]:

        query = (
            db.query(Sale)
            .order_by(Sale.id.desc())
        )

        total = query.count()

        offset = (page - 1) * page_size

        sales = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return sales, total

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
    def get_by_id_for_update(
        db: Session,
        sale_id: int,
    ) -> Sale | None:
        return (
            db.query(Sale)
            .filter(Sale.id == sale_id)
            .with_for_update()
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
