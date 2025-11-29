from fastapi import APIRouter, Depends
from sqlmodel import select

from app.models.models import Recommendation
from app.schemas.common import RecommendationRead
from app.utils.deps import get_db

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=list[RecommendationRead])
def list_recommendations(db=Depends(get_db)):
    return db.exec(select(Recommendation).order_by(Recommendation.created_at.desc()).limit(50)).all()
