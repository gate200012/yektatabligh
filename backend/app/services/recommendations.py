from datetime import datetime, timedelta
from collections import defaultdict
from sqlmodel import Session, select

from app.models.models import Post, PostAnalysis, Recommendation


ENGAGEMENT_THRESHOLD = 3
RECENT_HOURS = 12


def generate_reply_priority(session: Session):
    cutoff = datetime.utcnow() - timedelta(hours=RECENT_HOURS)
    results = (
        session.exec(
            select(Post, PostAnalysis)
            .join(PostAnalysis, Post.id == PostAnalysis.post_id)
            .where(PostAnalysis.sentiment == "negative", Post.published_at >= cutoff)
        )
        .all()
    )
    posts = []
    for post, analysis in results:
        engagement = post.like_count + post.comment_count + post.share_count
        if engagement >= ENGAGEMENT_THRESHOLD:
            posts.append({"post_id": post.id, "engagement": engagement, "source": post.source})
    if posts:
        session.add(Recommendation(type="reply_priority", data={"posts": posts}))


def generate_best_time(session: Session):
    buckets = defaultdict(list)
    posts = session.exec(select(Post)).all()
    for post in posts:
        if post.published_at:
            hour = post.published_at.hour
            buckets[(post.source, hour)].append(post.like_count + post.comment_count + post.share_count)
    best = []
    for (source, hour), values in buckets.items():
        avg = sum(values) / len(values)
        best.append({"source": source, "hour": hour, "score": avg})
    best = sorted(best, key=lambda x: x["score"], reverse=True)[:3]
    session.add(Recommendation(type="best_time_to_post", data={"slots": best}))


def generate_trending_topics(session: Session):
    # simplified trend detection based on keyword frequency
    counts = defaultdict(int)
    for analysis in session.exec(select(PostAnalysis)).all():
        for kw in analysis.keywords:
            counts[kw] += 1
    trending = sorted([{"keyword": k, "count": v} for k, v in counts.items()], key=lambda x: x["count"], reverse=True)[:5]
    if trending:
        session.add(Recommendation(type="trending_topic", data={"keywords": trending}))


def build_recommendations(session: Session):
    session.exec(select(Recommendation)).all()
    generate_reply_priority(session)
    generate_best_time(session)
    generate_trending_topics(session)
    session.commit()
