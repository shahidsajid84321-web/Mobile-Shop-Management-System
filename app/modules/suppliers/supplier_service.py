from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, NotFoundException

from app.models.supplier import Supplier
from app.modules.suppliers.supplier_repository import SupplierRepository
from app.modules.suppliers.supplier_schema import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)

from app.shared.pagination import (
    PaginationParams,
    PaginatedResponse,
)

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
            raise BadRequestException("Supplier already exists.")

        supplier = Supplier(**data.model_dump())

        return SupplierRepository.create(
            db,
            supplier,
        )

    @staticmethod
    def get_all(
        db: Session,
        pagination: PaginationParams,
    ) -> PaginatedResponse[SupplierResponse]:

        suppliers, total = SupplierRepository.get_all(
            db,
            pagination.page,
            pagination.page_size,
        )

        return PaginatedResponse.create(
            items=suppliers,
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        )

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
            raise NotFoundException("Supplier not found.")

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
            raise NotFoundException("Supplier not found.")

        updates = data.model_dump(exclude_unset=True)
        if "company_name" in updates:
            existing = SupplierRepository.get_by_company_name(
                db, updates["company_name"]
            )
            if existing and existing.id != supplier.id:
                raise BadRequestException("Supplier already exists.")

        for key, value in updates.items():
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
            raise NotFoundException("Supplier not found.")

        if supplier.purchases:
            raise BadRequestException("Supplier cannot be deleted because purchases are recorded for it.")

        SupplierRepository.delete(
            db,
            supplier,
        )
