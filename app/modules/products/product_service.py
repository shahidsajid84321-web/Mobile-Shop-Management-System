from sqlalchemy.orm import Session

from app.models.product import Product
from app.modules.categories.category_model import Category
from app.modules.products.product_repository import ProductRepository
from app.modules.products.product_schema import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(
        db: Session,
        product_data: ProductCreate,
    ) -> Product:

        # Check category exists
        category = (
            db.query(Category).filter(Category.id == product_data.category_id).first()
        )

        if category is None:
            raise ValueError("Category not found.")

        # Check duplicate SKU
        existing_product = (
            db.query(Product).filter(Product.sku == product_data.sku).first()
        )

        if existing_product:
            raise ValueError("SKU already exists.")

        product = Product(
            name=product_data.name,
            brand=product_data.brand,
            model_number=product_data.model_number,
            sku=product_data.sku,
            barcode=product_data.barcode,
            description=product_data.description,
            purchase_price=product_data.purchase_price,
            selling_price=product_data.selling_price,
            stock_quantity=product_data.stock_quantity,
            minimum_stock=product_data.minimum_stock,
            image=product_data.image,
            is_active=product_data.is_active,
            category_id=product_data.category_id,
        )

        return ProductRepository.create_product(
            db,
            product,
        )

    @staticmethod
    def get_all_products(
        db: Session,
    ) -> list[Product]:

        return ProductRepository.get_all_products(db)

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ) -> Product:

        product = ProductRepository.get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        return product

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
    ) -> Product:

        product = ProductRepository.get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        return ProductRepository.update_product(
            db,
            product,
        )

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ):

        product = ProductRepository.get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        ProductRepository.delete_product(
            db,
            product,
        )
