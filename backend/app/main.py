from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db
from app.core.config import get_settings
from app.api import auth, users, connectors, posts, categories, dashboard, recommendations, alerts
from app.services.scheduler import start_scheduler

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(users.router, prefix=settings.api_v1_str)
app.include_router(connectors.router, prefix=settings.api_v1_str)
app.include_router(posts.router, prefix=settings.api_v1_str)
app.include_router(categories.router, prefix=settings.api_v1_str)
app.include_router(dashboard.router, prefix=settings.api_v1_str)
app.include_router(recommendations.router, prefix=settings.api_v1_str)
app.include_router(alerts.router, prefix=settings.api_v1_str)


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()


@app.get("/")
def root():
    return {"message": "Social insight API running"}
