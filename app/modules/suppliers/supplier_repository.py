from sqlalchemy.orm import Session

from app.models.supplier import Supplier


class SupplierRepository:

    @staticmethod
    def create(
        db: Session,
        supplier: Supplier,
    ) -> Supplier:

        db.add(supplier)
        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def get_all(
        db: Session,
        page: int,
        page_size: int,
    ) -> tuple[list[Supplier], int]:

        query = db.query(Supplier)

        total = query.count()

        suppliers = (
            query
            .order_by(Supplier.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return suppliers, total

    @staticmethod
    def get_by_id(
        db: Session,
        supplier_id: int,
    ) -> Supplier | None:

        return db.query(Supplier).filter(Supplier.id == supplier_id).first()

    @staticmethod
    def get_by_company_name(
        db: Session,
        company_name: str,
    ) -> Supplier | None:

        return db.query(Supplier).filter(Supplier.company_name == company_name).first()

    @staticmethod
    def update(
        db: Session,
        supplier: Supplier,
    ) -> Supplier:

        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def delete(
        db: Session,
        supplier: Supplier,
    ):

        db.delete(supplier)
        db.commit()
