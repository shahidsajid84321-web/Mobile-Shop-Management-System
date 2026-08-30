from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.modules.roles.role_repository import RoleRepository
from app.modules.users.user_repository import UserRepository
from app.modules.users.user_schema import (
    UserCreate,
    UserUpdate,
)

from app.core.enums.roles import RoleName

from app.shared.pagination import (
    PaginatedResponse,
)


class UserService:

    @staticmethod
    def create(
        db: Session,
        data: UserCreate,
        actor: User,
    ) -> User:

        existing = UserRepository.get_by_email(
            db,
            data.email,
        )

        if existing:
            raise ValueError(
                "Email already registered."
            )

        role = RoleRepository.get_by_id(
            db,
            data.role_id,
        )

        if role is None:
            raise ValueError(
                "Role not found."
            )

        if role.name == RoleName.SUPER_ADMIN and actor.role.name != RoleName.SUPER_ADMIN:
            raise ValueError("Only a Super Admin can assign the Super Admin role.")

        user = User(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password),
            role_id=data.role_id,
            is_active=data.is_active,
            email_verified_at=datetime.now(UTC),
        )

        return UserRepository.create(
            db,
            user,
        )

    @staticmethod
    def get_paginated(
        db: Session,
        page: int,
        page_size: int,
    ) -> PaginatedResponse:

        users, total = UserRepository.get_paginated(
            db,
            page,
            page_size,
        )

        return PaginatedResponse.create(
            items=users,
            page=page,
            page_size=page_size,
            total=total,
        )     

    @staticmethod
    def get_one(
        db: Session,
        user_id: int,
    ) -> User:

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        return user

    @staticmethod
    def update(
        db: Session,
        user_id: int,
        data: UserUpdate,
        actor: User,
    ) -> User:

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        if user.role.name == RoleName.SUPER_ADMIN and actor.role.name != RoleName.SUPER_ADMIN:
            raise ValueError("Only a Super Admin can modify a Super Admin user.")

        updates = data.model_dump(
            exclude_unset=True,
        )

        if "email" in updates:

            existing = UserRepository.get_by_email(
                db,
                updates["email"],
            )

            if existing and existing.id != user.id:
                raise ValueError(
                    "Email already registered."
                )

        if "role_id" in updates:

            role = RoleRepository.get_by_id(
                db,
                updates["role_id"],
            )

            if role is None:
                raise ValueError(
                    "Role not found."
                )
            if role.name == RoleName.SUPER_ADMIN and actor.role.name != RoleName.SUPER_ADMIN:
                raise ValueError("Only a Super Admin can assign the Super Admin role.")

        if actor.id == user.id and (
            updates.get("is_active") is False
            or "role_id" in updates
        ):
            raise ValueError("You cannot deactivate yourself or change your own role.")

        if "password" in updates:

            updates["password"] = hash_password(
                updates["password"]
            )

        for key, value in updates.items():
            setattr(
                user,
                key,
                value,
            )

        return UserRepository.update(
            db,
            user,
        )

    @staticmethod
    def delete(
        db: Session,
        user_id: int,
        actor: User,
    ) -> None:

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        if user.role.name == RoleName.SUPER_ADMIN:
            raise ValueError(
                "Super Admin user cannot be deleted."
            )

        if actor.id == user.id:
            raise ValueError("You cannot delete your own account.")

        UserRepository.delete(
            db,
            user,
        )
      
