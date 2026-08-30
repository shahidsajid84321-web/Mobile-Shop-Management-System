from datetime import UTC, datetime, timedelta
from email.message import EmailMessage
import smtplib
import secrets

from sqlalchemy.orm import Session

from app.core.auth import hash_token
from app.core.config import settings
from app.core.exceptions import BadRequestException
from app.core.security import hash_password
from app.models.auth_session import AuthSession
from app.models.password_reset_token import PasswordResetToken
from app.modules.auth.auth_repository import AuthRepository


class PasswordResetService:
    @staticmethod
    def request_reset(db: Session, email: str) -> None:
        """Create a one-time reset token and email it without revealing account existence."""
        user = AuthRepository.get_user_by_email(db, email)
        if user is None or not user.is_active:
            return

        now = datetime.now(UTC)
        # Invalidate older outstanding reset tokens for this account.
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        ).update({PasswordResetToken.used_at: now}, synchronize_session=False)

        raw_token = secrets.token_urlsafe(48)
        expires_at = now + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES)
        reset_record = PasswordResetToken(
            user_id=user.id,
            token_hash=hash_token(raw_token),
            expires_at=expires_at,
            created_at=now,
        )
        db.add(reset_record)
        db.commit()

        try:
            PasswordResetService._send_reset_email(user.email, user.full_name, raw_token)
        except Exception:
            db.delete(reset_record)
            db.commit()
            raise

    @staticmethod
    def _send_reset_email(email: str, full_name: str, raw_token: str) -> None:
        if not all((settings.SMTP_HOST, settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_FROM_EMAIL)):
            raise RuntimeError("Password reset email service is not configured.")

        reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={raw_token}"
        message = EmailMessage()
        message["Subject"] = "Reset your Mobile Shop password"
        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = email
        message.set_content(
            f"Hello {full_name},\n\n"
            "We received a request to reset your Mobile Shop account password.\n\n"
            f"Reset your password here:\n{reset_url}\n\n"
            f"This link expires in {settings.PASSWORD_RESET_EXPIRE_MINUTES} minutes and can only be used once.\n\n"
            "If you did not request this, you can safely ignore this email.\n\n"
            "Mobile Shop"
        )

        if settings.SMTP_USE_TLS:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=settings.SMTP_TIMEOUT_SECONDS) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                smtp.send_message(message)
        else:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=settings.SMTP_TIMEOUT_SECONDS) as smtp:
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                smtp.send_message(message)

    @staticmethod
    def reset_password(db: Session, raw_token: str, new_password: str) -> None:
        now = datetime.now(UTC)
        token_hash = hash_token(raw_token)
        reset_record = (
            db.query(PasswordResetToken)
            .filter(PasswordResetToken.token_hash == token_hash)
            .with_for_update()
            .first()
        )

        if reset_record is None or reset_record.used_at is not None:
            raise BadRequestException("Invalid or expired password reset token.")

        expires_at = reset_record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= now:
            reset_record.used_at = now
            db.commit()
            raise BadRequestException("Invalid or expired password reset token.")

        user = AuthRepository.get_user_by_id(db, reset_record.user_id)
        if user is None or not user.is_active:
            reset_record.used_at = now
            db.commit()
            raise BadRequestException("Invalid or expired password reset token.")

        user.password = hash_password(new_password)
        reset_record.used_at = now

        # A password reset is a security event: invalidate every existing login.
        db.query(AuthSession).filter(
            AuthSession.user_id == user.id,
            AuthSession.revoked_at.is_(None),
        ).update({AuthSession.revoked_at: now}, synchronize_session=False)

        # Make every other outstanding reset link unusable too.
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.id != reset_record.id,
            PasswordResetToken.used_at.is_(None),
        ).update({PasswordResetToken.used_at: now}, synchronize_session=False)

        db.commit()
