from sqlalchemy.orm import Session

from app.modules.categories.category_model import Category
from app.modules.categories.category_repository import CategoryRepository
from app.modules.categories.category_schema import (CategoryCreate,
                                                    CategoryUpdate)


class CategoryService:

    @staticmethod
    def create_category(
        db: Session,
        category_data: CategoryCreate,
    ) -> Category:

        existing = CategoryRepository.get_by_name(
            db,
            category_data.name,
        )

        if existing:
            raise ValueError("Category already exists.")

        category = Category(
            name=category_data.name,
            description=category_data.description,
        )

        return CategoryRepository.create(
            db,
            category,
        )

    @staticmethod
    def get_categories(
        db: Session,
    ) -> list[Category]:
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_category(
        db: Session,
        category_id: int,
    ) -> Category:

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise ValueError("Category not found.")

        return category

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        category_data: CategoryUpdate,
    ) -> Category:

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise ValueError("Category not found.")

        if category_data.name is not None:
            category.name = category_data.name

        if category_data.description is not None:
            category.description = category_data.description

        return CategoryRepository.update(
            db,
            category,
        )

    @staticmethod
    def delete_category(
        db: Session,
        category_id: int,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise ValueError("Category not found.")

        CategoryRepository.delete(
            db,
            category,
        )
