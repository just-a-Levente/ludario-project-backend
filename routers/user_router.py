from fastapi import APIRouter, HTTPException, status
from repository.user_repository import UserRepository
from model.user import User
from schemas.user_api_schema import *
from services.log_service import log_service

user_router = APIRouter(prefix="/api/users", tags=["users"])
user_repo = UserRepository()


@user_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def register(request: RegisterRequest):
    if user_repo.get_user_by_email(request.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=request.email,
        username=request.username,
        password_hash=request.password_hash,
        roles=["admin"] if request.is_admin else ["user"],
    )

    user_repo.insert_user(user)
    permissions = list(user_repo.get_permissions_for_user(request.email))

    log_service.log(
        user_email=user.email,
        user_role=user.roles[0],
        action="REGISTER",
        details=f"New user registered for {request.email}"
    )
    return UserResponse(
        email=user.email,
        username=user.username,
        roles=user.roles,
        permissions=permissions
    )


@user_router.post(
    "/login",
    response_model=UserResponse
)
def login(request: LoginRequest):
    user = user_repo.get_user_by_email(request.email)

    if user is None or user.password_hash != request.password_hash:
        log_service.log(
            user_email=request.email,
            user_role="unknown" if user is None else (user.roles[0] if user.roles else "user"),
            action="LOGIN_FAILED",
            details=f"Failed login attempt for {request.email}"
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    permissions = list(user_repo.get_permissions_for_user(request.email))

    log_service.log(
        user_email=request.email,
        user_role=user.roles[0] if user.roles else "user",
        action="LOGIN",
        details=f"User {request.email} logged in"
    )
    return UserResponse(
        email=user.email,
        username=user.username,
        roles=user.roles,
        permissions=permissions
    )