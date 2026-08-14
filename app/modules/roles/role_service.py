from sqlalchemy.orm import Session

from app.models.role import Role
from app.modules.roles.role_repository import RoleRepository
from app.modules.roles.role_schema import (
    RoleCreate,
    RoleUpdate,
)

from app.core.enums.roles import RoleName

class RoleService:

    @staticmethod
    def create(
        db: Session,
        data: RoleCreate,
    ) -> Role:

        existing = RoleRepository.get_by_name(
            db,
            data.name,
        )

        if existing:
            raise ValueError(
                "Role already exists."
            )

        role = Role(
            name=data.name,
            description=data.description,
        )

        return RoleRepository.create(
            db,
            role,
        )

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Role]:

        return RoleRepository.get_all(db)

    @staticmethod
    def get_one(
        db: Session,
        role_id: int,
    ) -> Role:

        role = RoleRepository.get_by_id(
            db,
            role_id,
        )

        if role is None:
            raise ValueError(
                "Role not found."
            )

        return role

    @staticmethod
    def update(
        db: Session,
        role_id: int,
        data: RoleUpdate,
    ) -> Role:

        role = RoleRepository.get_by_id(
            db,
            role_id,
        )

        if role is None:
            raise ValueError(
                "Role not found."
            )

        updates = data.model_dump(
            exclude_unset=True,
        )

        # Protect Super Admin role
        if role.name == RoleName.SUPER_ADMIN:
            if (
                "name" in updates
                and updates["name"] != RoleName.SUPER_ADMIN
            ):
                raise ValueError(
                    "Super Admin role cannot be renamed."
                )

        if "name" in updates:

            existing = RoleRepository.get_by_name(
                db,
                updates["name"],
            )

            if existing and existing.id != role.id:
                raise ValueError(
                    "Role already exists."
                )

        for key, value in updates.items():
            setattr(
                role,
                key,
                value,
            )

        return RoleRepository.update(
            db,
            role,
        )

    @staticmethod
    def delete(
        db: Session,
        role_id: int,
    ) -> None:

        role = RoleRepository.get_by_id(
            db,
            role_id,
        )

        if role is None:
            raise ValueError(
                "Role not found."
            )

        # Protect Super Admin role
        if role.name == RoleName.SUPER_ADMIN:
            raise ValueError(
                "Super Admin role cannot be deleted."
            )

        # Prevent deletion when users are assigned
        if role.users:
            raise ValueError(
                "Role cannot be deleted because users are assigned to it."
            )

        RoleRepository.delete(
            db,
            role,
        )