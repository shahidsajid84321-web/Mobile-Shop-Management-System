from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.auth import create_access_token, create_refresh_token, hash_token
from app.core.config import settings
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import hash_password, verify_password
from app.models.auth_session import AuthSession
from app.models.customer import Customer
from app.models.login_rate_limit import LoginRateLimit
from app.models.role import Role
from app.models.user import User
from app.modules.auth.auth_repository import AuthRepository
from app.modules.auth.email_verification import EmailVerificationService
from app.modules.auth.auth_schema import Token, UserLogin, UserRegister


class AuthService:

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        existing_user = AuthRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            raise BadRequestException("Email already registered.")

        hashed_password = hash_password(user_data.password)
        customer_role = db.query(Role).filter(Role.name == "Customer").first()
        if customer_role is None:
            raise BadRequestException("Customer role not found.")

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            role_id=customer_role.id,
        )

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
            db.flush()
            EmailVerificationService.create_and_send(db, created_user)
            db.commit()
            db.refresh(created_user)
            return created_user
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def _issue_session(db: Session, user: User) -> tuple[Token, str, datetime]:
        access_token, access_jti, access_expires_at = create_access_token(
            data={"sub": str(user.id), "role": user.role.name}
        )
        refresh_token, refresh_hash, refresh_expires_at = create_refresh_token()

        session = AuthSession(
            user_id=user.id,
            refresh_token_hash=refresh_hash,
            access_jti=access_jti,
            access_expires_at=access_expires_at,
            refresh_expires_at=refresh_expires_at,
            created_at=datetime.now(UTC),
        )
        db.add(session)
        db.commit()

        expires_in = max(0, int((access_expires_at - datetime.now(UTC)).total_seconds()))
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        ), refresh_token, refresh_expires_at

    @staticmethod
    def _get_login_rate_limit(db: Session, email: str, ip_address: str) -> LoginRateLimit | None:
        return (
            db.query(LoginRateLimit)
            .filter(
                LoginRateLimit.email == email,
                LoginRateLimit.ip_address == ip_address,
            )
            .with_for_update()
            .first()
        )

    @staticmethod
    def _check_login_rate_limit(db: Session, email: str, ip_address: str) -> None:
        now = datetime.now(UTC)
        state = AuthService._get_login_rate_limit(db, email, ip_address)
        if state is None:
            state = LoginRateLimit(
                email=email,
                ip_address=ip_address,
                failed_attempts=0,
                window_started_at=now,
                last_attempt_at=now,
            )
            db.add(state)
            db.flush()
            return

        window_started = state.window_started_at
        if window_started.tzinfo is None:
            window_started = window_started.replace(tzinfo=UTC)

        if now - window_started >= timedelta(seconds=settings.LOGIN_WINDOW_SECONDS):
            state.failed_attempts = 0
            state.window_started_at = now
            state.locked_until = None

        locked_until = state.locked_until
        if locked_until is not None:
            if locked_until.tzinfo is None:
                locked_until = locked_until.replace(tzinfo=UTC)
            if locked_until > now:
                retry_after = max(1, int((locked_until - now).total_seconds()))
                raise UnauthorizedException(
                    f"Too many failed login attempts. Please try again in about {retry_after} seconds."
                )
            state.locked_until = None
            state.failed_attempts = 0
            state.window_started_at = now

    @staticmethod
    def _record_login_failure(db: Session, email: str, ip_address: str) -> None:
        now = datetime.now(UTC)
        state = AuthService._get_login_rate_limit(db, email, ip_address)
        if state is None:
            state = LoginRateLimit(
                email=email,
                ip_address=ip_address,
                failed_attempts=0,
                window_started_at=now,
                last_attempt_at=now,
            )
            db.add(state)
            db.flush()

        window_started = state.window_started_at
        if window_started.tzinfo is None:
            window_started = window_started.replace(tzinfo=UTC)
        if now - window_started >= timedelta(seconds=settings.LOGIN_WINDOW_SECONDS):
            state.failed_attempts = 0
            state.window_started_at = now
            state.locked_until = None

        state.failed_attempts += 1
        state.last_attempt_at = now
        if state.failed_attempts >= settings.LOGIN_MAX_ATTEMPTS:
            state.locked_until = now + timedelta(seconds=settings.LOGIN_LOCKOUT_SECONDS)
        db.commit()

    @staticmethod
    def _clear_login_failures(db: Session, email: str, ip_address: str) -> None:
        state = AuthService._get_login_rate_limit(db, email, ip_address)
        if state is not None:
            db.delete(state)

    @staticmethod
    def login_user(db: Session, user_data: UserLogin, ip_address: str = "unknown") -> tuple[Token, str, datetime]:
        email = str(user_data.email).strip().lower()
        ip_address = ip_address or "unknown"

        # Rate-limit before checking credentials, including unknown accounts, to prevent
        # attackers from bypassing the limiter by rotating through nonexistent emails.
        AuthService._check_login_rate_limit(db, email, ip_address)

        try:
            user = AuthRepository.get_user_by_email(db, email)
            if not user:
                raise UnauthorizedException("Invalid email or password.")
            if not user.is_active:
                raise UnauthorizedException("User account is inactive.")
            if user.email_verified_at is None:
                raise UnauthorizedException("Please verify your email address before logging in.")
            if not verify_password(user_data.password, user.password):
                raise UnauthorizedException("Invalid email or password.")

            AuthService._clear_login_failures(db, email, ip_address)
            return AuthService._issue_session(db, user)
        except UnauthorizedException:
            AuthService._record_login_failure(db, email, ip_address)
            raise
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def refresh_session(db: Session, refresh_token: str) -> tuple[Token, str, datetime]:
        token_hash = hash_token(refresh_token)
        session = (
            db.query(AuthSession)
            .filter(AuthSession.refresh_token_hash == token_hash)
            .with_for_update()
            .first()
        )
        now = datetime.now(UTC)

        if session is None or session.revoked_at is not None:
            raise UnauthorizedException("Invalid or expired refresh token.")

        refresh_expires_at = session.refresh_expires_at
        if refresh_expires_at.tzinfo is None:
            refresh_expires_at = refresh_expires_at.replace(tzinfo=UTC)
        if refresh_expires_at <= now:
            raise UnauthorizedException("Invalid or expired refresh token.")

        user = AuthRepository.get_user_by_id(db, session.user_id)
        if user is None:
            session.revoked_at = now
            db.commit()
            raise UnauthorizedException("User not found.")
        if not user.is_active:
            session.revoked_at = now
            db.commit()
            raise UnauthorizedException("User account is inactive.")

        access_token, access_jti, access_expires_at = create_access_token(
            data={"sub": str(user.id), "role": user.role.name}
        )
        new_refresh_token, new_refresh_hash, new_refresh_expires_at = create_refresh_token()

        session.refresh_token_hash = new_refresh_hash
        session.access_jti = access_jti
        session.access_expires_at = access_expires_at
        session.refresh_expires_at = new_refresh_expires_at
        session.last_used_at = now
        db.commit()

        expires_in = max(0, int((access_expires_at - datetime.now(UTC)).total_seconds()))
        return (
            Token(access_token=access_token, token_type="bearer", expires_in=expires_in),
            new_refresh_token,
            new_refresh_expires_at,
        )

    @staticmethod
    def revoke_refresh_token(db: Session, refresh_token: str) -> None:
        session = (
            db.query(AuthSession)
            .filter(AuthSession.refresh_token_hash == hash_token(refresh_token))
            .first()
        )
        if session is not None and session.revoked_at is None:
            session.revoked_at = datetime.now(UTC)
            db.commit()
