from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.modules.suppliers.supplier_repository import SupplierRepository
from app.modules.suppliers.supplier_schema import (SupplierCreate,
                                                   SupplierUpdate)


class SupplierService:

    @staticmethod
    def create(
        db: Session,
        data: SupplierCreate,
    ) -> Supplier:

        existing = SupplierRepository.get_by_company_name(
            db,
            data.company_name,
        )

        if existing:
            raise ValueError("Supplier already exists.")

        supplier = Supplier(**data.model_dump())

        return SupplierRepository.create(
            db,
            supplier,
        )

    @staticmethod
    def get_all(
        db: Session,
    ):
        return SupplierRepository.get_all(db)

    @staticmethod
    def get_one(
        db: Session,
        supplier_id: int,
    ):

        supplier = SupplierRepository.get_by_id(
            db,
            supplier_id,
        )

        if supplier is None:
            raise ValueError("Supplier not found.")

        return supplier

    @staticmethod
    def update(
        db: Session,
        supplier_id: int,
        data: SupplierUpdate,
    ):

        supplier = SupplierRepository.get_by_id(
            db,
            supplier_id,
        )

        if supplier is None:
            raise ValueError("Supplier not found.")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(
                supplier,
                key,
                value,
            )

        return SupplierRepository.update(
            db,
            supplier,
        )

    @staticmethod
    def delete(
        db: Session,
        supplier_id: int,
    ):

        supplier = SupplierRepository.get_by_id(
            db,
            supplier_id,
        )

        if supplier is None:
            raise ValueError("Supplier not found.")

        SupplierRepository.delete(
            db,
            supplier,
        )
