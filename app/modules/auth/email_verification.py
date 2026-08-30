from datetime import UTC, datetime, timedelta
from email.message import EmailMessage
import secrets
import smtplib

from sqlalchemy.orm import Session

from app.core.auth import hash_token
from app.core.config import settings
from app.core.exceptions import BadRequestException
from app.models.email_verification_token import EmailVerificationToken
from app.models.user import User
from app.modules.auth.auth_repository import AuthRepository


class EmailVerificationService:
    @staticmethod
    def create_and_send(db: Session, user: User) -> None:
        now = datetime.now(UTC)
        db.query(EmailVerificationToken).filter(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used_at.is_(None),
        ).update({EmailVerificationToken.used_at: now}, synchronize_session=False)

        raw_token = secrets.token_urlsafe(48)
        expires_at = now + timedelta(minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES)
        record = EmailVerificationToken(
            user_id=user.id,
            token_hash=hash_token(raw_token),
            expires_at=expires_at,
            created_at=now,
        )
        db.add(record)
        db.flush()

        try:
            EmailVerificationService._send_email(user.email, user.full_name, raw_token)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def _send_email(email: str, full_name: str, raw_token: str) -> None:
        if not all((settings.SMTP_HOST, settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_FROM_EMAIL)):
            raise RuntimeError("Email delivery service is not configured.")

        verify_url = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={raw_token}"
        message = EmailMessage()
        message["Subject"] = "Verify your Mobile Shop email"
        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = email
        message.set_content(
            f"Hello {full_name},\n\n"
            "Thank you for creating a Mobile Shop account. Please verify your email address using the link below:\n\n"
            f"{verify_url}\n\n"
            f"This link expires in {settings.EMAIL_VERIFICATION_EXPIRE_MINUTES} minutes and can only be used once.\n\n"
            "If you did not create this account, you can safely ignore this email.\n\n"
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
    def verify(db: Session, raw_token: str) -> None:
        now = datetime.now(UTC)
        record = (
            db.query(EmailVerificationToken)
            .filter(EmailVerificationToken.token_hash == hash_token(raw_token))
            .with_for_update()
            .first()
        )

        if record is None or record.used_at is not None:
            raise BadRequestException("Invalid or expired email verification token.")

        expires_at = record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= now:
            record.used_at = now
            db.commit()
            raise BadRequestException("Invalid or expired email verification token.")

        user = AuthRepository.get_user_by_id(db, record.user_id)
        if user is None:
            record.used_at = now
            db.commit()
            raise BadRequestException("Invalid or expired email verification token.")

        user.email_verified_at = now
        record.used_at = now
        db.query(EmailVerificationToken).filter(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.id != record.id,
            EmailVerificationToken.used_at.is_(None),
        ).update({EmailVerificationToken.used_at: now}, synchronize_session=False)
        db.commit()

    @staticmethod
    def resend(db: Session, email: str) -> None:
        user = AuthRepository.get_user_by_email(db, email)
        if user is None or not user.is_active or user.email_verified_at is not None:
            return

        latest = (
            db.query(EmailVerificationToken)
            .filter(EmailVerificationToken.user_id == user.id)
            .order_by(EmailVerificationToken.created_at.desc())
            .first()
        )
        if latest is not None:
            created_at = latest.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)
            if (datetime.now(UTC) - created_at).total_seconds() < settings.EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS:
                return

        EmailVerificationService.create_and_send(db, user)
