from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.dependencies.role_dependency import require_roles

from app.modules.auth.auth_schema import (
    UserRegister,
    UserResponse,
    UserLogin,
    Token,
)

from app.modules.auth.dependencies import get_current_user
from app.models.user import User

from app.modules.auth.auth_service import AuthService

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
        require_roles("Super Admin"),
    ),
):
    return {
        "message": "Welcome Super Admin!",
        "user": current_user.full_name,
    }