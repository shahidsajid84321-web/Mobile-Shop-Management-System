from sqlalchemy.orm import Session

from app.models.purchase_item import PurchaseItem


class PurchaseItemRepository:

    @staticmethod
    def create(
        db: Session,
        purchase_item: PurchaseItem,
    ) -> PurchaseItem:

        db.add(purchase_item)

        return purchase_item
