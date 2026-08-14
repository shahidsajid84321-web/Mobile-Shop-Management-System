from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def create(
        db: Session,
        user: User,
    ) -> User:

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_paginated(
        db: Session,
        page: int,
        limit: int,
    ) -> tuple[list[User], int]:

        query = (
            db.query(User)
            .order_by(User.id.desc())
        )

        total = query.count()

        offset = (page - 1) * limit

        users = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return users, total 

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        user: User,
    ) -> User:

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete(
        db: Session,
        user: User,
    ) -> None:

        db.delete(user)
        db.commit()      
   