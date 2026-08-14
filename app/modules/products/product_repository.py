from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    @staticmethod
    def create_product(
        db: Session,
        product: Product,
    ) -> Product:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_paginated(
        db: Session,
        page: int,
        page_size: int,
    ) -> tuple[list[Product], int]:
        query = (
            db.query(Product)
            .order_by(Product.id.desc())
        )

        total = query.count()
        offset = (page - 1) * page_size

        products = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return products, total

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int,
    ) -> Product | None:
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def get_by_id_for_update(
        db: Session,
        product_id: int,
    ) -> Product | None:
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .with_for_update()
            .first()
        )

    @staticmethod
    def update_product(
        db: Session,
        product: Product,
    ) -> Product:
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(
        db: Session,
        product: Product,
    ) -> None:
        db.delete(product)
        db.commit()
