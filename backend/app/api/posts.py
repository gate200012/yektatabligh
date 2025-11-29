from fastapi import APIRouter, Depends
from sqlmodel import select

from app.models.models import Post, PostAnalysis, PostCategory
from app.schemas.common import PostRead, PostFilter
from app.utils.deps import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostRead])
def list_posts(filters: PostFilter = Depends(), db=Depends(get_db)):
    query = select(Post)
    if filters.source:
        query = query.where(Post.source == filters.source)
    if filters.from_date:
        query = query.where(Post.published_at >= filters.from_date)
    if filters.to_date:
        query = query.where(Post.published_at <= filters.to_date)
    posts = db.exec(query.order_by(Post.created_at.desc()).limit(200)).all()
    return posts


@router.get("/{post_id}")
def read_post(post_id: int, db=Depends(get_db)):
    post = db.get(Post, post_id)
    analysis = db.exec(select(PostAnalysis).where(PostAnalysis.post_id == post_id)).first()
    categories = db.exec(select(PostCategory).where(PostCategory.post_id == post_id)).all()
    return {"post": post, "analysis": analysis, "categories": categories}
