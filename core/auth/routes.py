from fastapi import APIRouter, HTTPException

from core.auth.models import User
from core.auth.schemas import LoginResponse, UserCreate, UserLogin, UserResponse
from core.shared.conf import settings
from tortoise.expressions import Q

from core.shared.auth import create_tokens

auth_route = APIRouter()


@auth_route.post("/signup/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_obj =  User.filter(
        Q(username=user.username) | Q(email=user.email)
    )
    if await user_obj.exists():
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    new_user.set_password(user.password)
    await new_user.save()
    return new_user


@auth_route.post("/login/", response_model = LoginResponse)
async def login_user(user_login: UserLogin):
    user = await User.filter(username=user_login.username).first()
    if not user or not user.check_password(user_login.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate access and refresh tokens
    access_token, refresh_token = create_tokens(user)
    access_expiry = settings.JWT_EXPIRATION_TIME * 60
    refresh_expiry = settings.JWT_REFRESH_EXPIRATION_TIME * 60
    return {
        "access_token": access_token,
        "access_expiry": access_expiry,
        "refresh_token": refresh_token,
        "refresh_expiry": refresh_expiry,
        "status": True
    }