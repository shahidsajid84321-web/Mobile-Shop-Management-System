from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import hash_password, verify_password
from app.models.role import Role
from app.models.user import User
from app.models.customer import Customer
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

        customer_role = (
            db.query(Role)
            .filter(Role.name == "Customer")
            .first()
        )

        if customer_role is None:
            raise BadRequestException(
                "Customer role not found."
            )

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            role_id=customer_role.id,
        )

        # Save user and create customer profile in one transaction.
        try:
            created_user = AuthRepository.create_user(db, new_user)
            customer = None
            if created_user.phone:
                customer = db.query(Customer).filter(Customer.phone == created_user.phone).first()
            if customer is None:
                customer = db.query(Customer).filter(Customer.email == created_user.email).first()
            if customer is None:
                customer = Customer(
                    user_id=created_user.id,
                    full_name=created_user.full_name,
                    email=created_user.email,
                    phone=created_user.phone or f"user-{created_user.id}",
                )
                db.add(customer)
            else:
                if customer.user_id and customer.user_id != created_user.id:
                    raise BadRequestException("Customer is already linked to another account.")
                customer.user_id = created_user.id
                customer.full_name = created_user.full_name
                customer.email = created_user.email
            db.commit()
            db.refresh(created_user)
            return created_user
        except Exception:
            db.rollback()
            raise

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

        if not user.is_active:
            raise UnauthorizedException(
                "User account is inactive."
            )

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
