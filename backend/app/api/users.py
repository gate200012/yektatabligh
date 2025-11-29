from fastapi import APIRouter, Depends

from app.schemas.auth import UserRead
from app.utils.deps import get_current_user

router = APIRouter(prefix="/me", tags=["users"])


@router.get("", response_model=UserRead)
def read_me(user=Depends(get_current_user)):
    return user
