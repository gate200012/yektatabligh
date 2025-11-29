from fastapi import APIRouter, Depends
from sqlmodel import select

from app.models.models import Alert
from app.schemas.common import AlertRead
from app.utils.deps import get_db

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def list_alerts(db=Depends(get_db)):
    return db.exec(select(Alert).order_by(Alert.created_at.desc()).limit(50)).all()
