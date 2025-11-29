from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.core.config import get_settings
from app.core.db import get_session
from app.models.models import User
from app.schemas.auth import Token, UserCreate, UserRead
from app.utils.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate):
    with get_session() as session:
        existing = session.exec(select(User).where(User.email == user_in.email)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(email=user_in.email, password_hash=get_password_hash(user_in.password), role=user_in.role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_session() as session:
        user = session.exec(select(User).where(User.email == form_data.username)).first()
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(user.email, access_token_expires)
        return Token(access_token=access_token)
