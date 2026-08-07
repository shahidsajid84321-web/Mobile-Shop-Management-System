from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.modules.auth.auth_repository import AuthRepository
from app.modules.auth.auth_schema import Token, UserLogin, UserRegister


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserRegister,
    ) -> User:

        # Check if email already exists
        existing_user = AuthRepository.get_user_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise BadRequestException("Email already registered.")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create User object
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            role_id=user_data.role_id,
        )

        # Save user
        return AuthRepository.create_user(
            db,
            new_user,
        )

    @staticmethod
    def login_user(
        db: Session,
        user_data: UserLogin,
    ) -> Token:

        # Find user by email
        user = AuthRepository.get_user_by_email(
            db,
            user_data.email,
        )

        if not user:
            raise UnauthorizedException("Invalid email or password.")

        # Verify password
        if not verify_password(
            user_data.password,
            user.password,
        ):
            raise UnauthorizedException("Invalid email or password.")

        # Generate JWT
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "role": user.role.name,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )
