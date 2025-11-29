from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlmodel import select, func

from app.models.models import Post, PostAnalysis
from app.utils.deps import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
def overview(db=Depends(get_db)):
    total_posts = db.exec(select(func.count(Post.id))).first()
    sentiments = {
        sentiment: db.exec(select(func.count(PostAnalysis.id)).where(PostAnalysis.sentiment == sentiment)).first()
        for sentiment in ["positive", "negative", "neutral"]
    }
    recent_posts = db.exec(select(Post).order_by(Post.created_at.desc()).limit(20)).all()
    return {"total_posts": total_posts, "sentiments": sentiments, "recent_posts": recent_posts}
