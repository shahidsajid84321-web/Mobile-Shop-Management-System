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
    ) -> list[Supplier]:

        return db.query(Supplier).all()

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
