from sqlalchemy.orm import Session

from app.models.sale_item import SaleItem


class SaleItemRepository:

    @staticmethod
    def create(
        db: Session,
        sale_item: SaleItem,
    ) -> SaleItem:

        db.add(sale_item)

        return sale_item
