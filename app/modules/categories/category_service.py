from sqlalchemy.orm import Session


from app.modules.categories.category_model import Category
from app.modules.categories.category_repository import CategoryRepository
from app.modules.categories.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)

from app.shared.pagination import (
    PaginatedResponse,
)

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
    def get_paginated(
        db: Session,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[CategoryResponse]:

        categories, total = CategoryRepository.get_paginated(
            db,
            page,
            page_size,
        )

        return PaginatedResponse.create(
            items=categories,
            page=page,
            page_size=page_size,
            total=total,
        )    

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
            existing = CategoryRepository.get_by_name(db, category_data.name)
            if existing and existing.id != category.id:
                raise ValueError("Category already exists.")

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

        if category.products:
            raise ValueError("Category cannot be deleted because products are assigned to it.")

        CategoryRepository.delete(
            db,
            category,
        )
