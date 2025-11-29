from datetime import datetime, timedelta
from sqlmodel import Session, select

from app.models.models import PostAnalysis, Alert


def generate_sentiment_alerts(session: Session, window_minutes: int = 60):
    cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
    analyses = session.exec(select(PostAnalysis).where(PostAnalysis.created_at >= cutoff)).all()
    if not analyses:
        return
    negatives = [a for a in analyses if a.sentiment == "negative"]
    ratio = len(negatives) / len(analyses)
    level = None
    if ratio > 0.7:
        level = "critical"
    elif ratio > 0.5:
        level = "warning"
    if level:
        alert = Alert(level=level, message="افزایش احساسات منفی", data={"ratio": ratio})
        session.add(alert)
        session.commit()
