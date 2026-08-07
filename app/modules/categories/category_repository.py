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
    def get_all(
        db: Session,
    ) -> list[Category]:
        return (
            db.query(Category)
            .order_by(Category.id)
            .all()
        )

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