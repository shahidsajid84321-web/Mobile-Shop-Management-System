from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.enums.roles import RoleName
from app.dependencies.db import get_db
from app.dependencies.role_dependency import require_roles
from app.models.user import User
from app.modules.auth.auth_schema import (
    PasswordResetConfirm,
    EmailVerificationRequest,
    EmailVerificationConfirm,
    PasswordResetRequest,
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.modules.auth.auth_service import AuthService
from app.modules.auth.password_reset import PasswordResetService
from app.modules.auth.email_verification import EmailVerificationService
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _set_refresh_cookie(response: Response, refresh_token: str, expires_at: datetime) -> None:
    max_age = max(0, int((expires_at - datetime.now(UTC)).total_seconds()))
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=max_age,
        expires=max_age,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        path="/auth",
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        path="/auth",
    )


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if not settings.ALLOW_PUBLIC_REGISTRATION:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Public registration is disabled.")
    return AuthService.register_user(db=db, user_data=user)


@router.post("/login", response_model=Token)
def login(request: Request, user: UserLogin, response: Response, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    token, refresh_token, refresh_expires_at = AuthService.login_user(
        db=db, user_data=user, ip_address=client_ip
    )
    _set_refresh_cookie(response, refresh_token, refresh_expires_at)
    return token


@router.post("/refresh", response_model=Token)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is required.")
    token, new_refresh_token, refresh_expires_at = AuthService.refresh_session(db, refresh_token)
    _set_refresh_cookie(response, new_refresh_token, refresh_expires_at)
    return token


@router.post("/email-verification/verify", status_code=200)
def verify_email(data: EmailVerificationConfirm, db: Session = Depends(get_db)):
    EmailVerificationService.verify(db, data.token)
    return {"message": "Email verified successfully. You can now log in."}


@router.post("/email-verification/resend", status_code=202)
def resend_email_verification(data: EmailVerificationRequest, db: Session = Depends(get_db)):
    # Do not disclose whether an email belongs to an account.
    EmailVerificationService.resend(db, data.email)
    return {"message": "If the account exists and is not verified, a verification email has been sent."}


@router.post("/password-reset/request", status_code=202)
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    # Always return the same response so account existence is not disclosed.
    PasswordResetService.request_reset(db, data.email)
    return {"message": "If an account exists for this email, a password reset link has been sent."}


@router.post("/password-reset/confirm", status_code=200)
def confirm_password_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    PasswordResetService.reset_password(db, data.token, data.new_password)
    return {"message": "Password reset successful. Please log in with your new password."}


@router.post("/logout", status_code=204)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if refresh_token:
        AuthService.revoke_refresh_token(db, refresh_token)
    _clear_refresh_cookie(response)
    return Response(status_code=204)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin-test")
def admin_test(current_user: User = Depends(require_roles(RoleName.SUPER_ADMIN))):
    return {"message": "Welcome Super Admin!", "user": current_user.full_name}
