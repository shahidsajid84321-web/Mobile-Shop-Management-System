from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    @staticmethod
    def create(
        db: Session,
        role: Role,
    ) -> Role:

        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Role]:

        return (
            db.query(Role)
            .order_by(Role.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        role_id: int,
    ) -> Role | None:

        return (
            db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str,
    ) -> Role | None:

        return (
            db.query(Role)
            .filter(Role.name == name)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        role: Role,
    ) -> Role:

        db.commit()
        db.refresh(role)

        return role

    @staticmethod
    def delete(
        db: Session,
        role: Role,
    ) -> None:

        db.delete(role)
        db.commit()