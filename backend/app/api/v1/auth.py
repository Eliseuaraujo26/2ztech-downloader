"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DbSession
from app.schemas.user import UserCreate, UserLogin, TokenResponse, TokenRefresh, UserResponse
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DbSession):
    service = AuthService(db)
    try:
        user = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return service.create_tokens(user)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: DbSession):
    service = AuthService(db)
    user = await service.authenticate(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return service.create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: TokenRefresh, db: DbSession):
    service = AuthService(db)
    tokens = await service.refresh_tokens(data.refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return tokens


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser):
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: CurrentUser):
    return MessageResponse(message="Logged out successfully")
