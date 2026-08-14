from sqlalchemy.orm import Session

from app.modules.categories.category_model import Category


class CategoryRepository:

    @staticmethod
    def create(
        db: Session,
        category: Category,
    ) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_paginated(
        db: Session,
        page: int,
        page_size: int,
    ) -> tuple[list[Category], int]:
        query = (
            db.query(Category)
            .order_by(Category.id.desc())
        )

        total = query.count()
        offset = (page - 1) * page_size

        categories = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return categories, total

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: int,
    ) -> Category | None:
        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str,
    ) -> Category | None:
        return (
            db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        category: Category,
    ) -> Category:
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(
        db: Session,
        category: Category,
    ) -> None:
        db.delete(category)
        db.commit()
