from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.role_dependency import require_roles
from app.models.user import User
from app.modules.auth.auth_schema import (Token,
    UserLogin,
    UserRegister,
    UserResponse,
    )

from app.modules.auth.auth_service import AuthService
from app.modules.auth.dependencies import get_current_user

from app.core.enums.roles import RoleName
from app.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    if not settings.ALLOW_PUBLIC_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public registration is disabled.",
        )
    return AuthService.register_user(
        db=db,
        user_data=user,
    )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return AuthService.login_user(
        db=db,
        user_data=user,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(
        require_roles(RoleName.SUPER_ADMIN),
    ),
):
    return {
        "message": "Welcome Super Admin!",
        "user": current_user.full_name,
    }
