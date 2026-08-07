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
    def get_all_products(
        db: Session,
    ) -> list[Product]:

        return db.query(Product).all()

    @staticmethod
    def get_product_by_id(
        db: Session,
        product_id: int,
    ) -> Product | None:

        return db.query(Product).filter(Product.id == product_id).first()

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
