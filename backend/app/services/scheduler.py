from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import select

from app.core.db import get_session
from app.core.config import get_settings
from app.models.models import SocialConnector
from app.services.connectors import ingest_connector
from app.services.analysis import analyze_new_posts
from app.services.recommendations import build_recommendations
from app.services.alerts import generate_sentiment_alerts

settings = get_settings()
scheduler = BackgroundScheduler()


def run_ingestion_job():
    with get_session() as session:
        connectors = session.exec(select(SocialConnector).where(SocialConnector.is_active == True)).all()
        for connector in connectors:
            posts = ingest_connector(session, connector)
            analyze_new_posts(session, posts)
        build_recommendations(session)
        generate_sentiment_alerts(session)


def start_scheduler():
    scheduler.add_job(run_ingestion_job, "interval", minutes=settings.scheduler_interval_minutes, id="ingestion")
    scheduler.start()
