from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_transaction import StockTransaction
from app.modules.categories.category_model import Category
from app.modules.products.product_repository import ProductRepository
from app.modules.products.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

from app.shared.pagination import (
    PaginatedResponse,
)


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

        # Keep initial stock auditable just like later adjustments.
        db.add(product)
        db.flush()
        if product.stock_quantity:
            db.add(
                StockTransaction(
                    product_id=product.id,
                    transaction_type="IN",
                    quantity=product.stock_quantity,
                    unit_price=product.purchase_price,
                    remarks="Initial product stock",
                )
            )
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_paginated(
        db: Session,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[ProductResponse]:

        products, total = ProductRepository.get_paginated(
            db,
            page,
            page_size,
        )

        return PaginatedResponse.create(
            items=products,
            page=page,
            page_size=page_size,
            total=total,
        )

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ) -> Product:

        product = ProductRepository.get_by_id(
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

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        update_data = product_data.model_dump(exclude_unset=True)

        if "stock_quantity" in update_data:
            raise ValueError(
                "Stock quantity must be changed through inventory adjustments."
            )

        if "category_id" in update_data and (
            db.query(Category)
            .filter(Category.id == update_data["category_id"])
            .first() is None
        ):
            raise ValueError("Category not found.")

        if "sku" in update_data:
            existing = (
                db.query(Product)
                .filter(Product.sku == update_data["sku"])
                .first()
            )
            if existing and existing.id != product.id:
                raise ValueError("SKU already exists.")

        if "barcode" in update_data and update_data["barcode"] is not None:
            existing = (
                db.query(Product)
                .filter(Product.barcode == update_data["barcode"])
                .first()
            )
            if existing and existing.id != product.id:
                raise ValueError("Barcode already exists.")

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

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        if product.purchase_items or product.sale_items or product.stock_transactions:
            raise ValueError(
                "Product cannot be deleted because it has inventory or transaction history."
            )

        ProductRepository.delete_product(
            db,
            product,
        )
