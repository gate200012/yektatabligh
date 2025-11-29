from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.models.models import SocialConnector
from app.schemas.common import ConnectorCreate, ConnectorRead
from app.utils.deps import get_db, require_role
from app.services.connectors import ingest_connector
from app.services.analysis import analyze_new_posts

router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.get("", response_model=list[ConnectorRead])
def list_connectors(db=Depends(get_db)):
    return db.exec(select(SocialConnector)).all()


@router.post("", response_model=ConnectorRead, dependencies=[Depends(require_role("admin", "analyst"))])
def create_connector(connector_in: ConnectorCreate, db=Depends(get_db), user=Depends(require_role("admin", "analyst"))):
    connector = SocialConnector(**connector_in.dict(), created_by=user.id)
    db.add(connector)
    db.commit()
    db.refresh(connector)
    return connector


@router.patch("/{connector_id}", response_model=ConnectorRead, dependencies=[Depends(require_role("admin", "analyst"))])
def update_connector(connector_id: int, connector_in: ConnectorCreate, db=Depends(get_db)):
    connector = db.get(SocialConnector, connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    for k, v in connector_in.dict().items():
        setattr(connector, k, v)
    db.commit()
    db.refresh(connector)
    return connector


@router.post("/{connector_id}/sync")
def sync_connector(connector_id: int, db=Depends(get_db)):
    connector = db.get(SocialConnector, connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    posts = ingest_connector(db, connector)
    analyses = analyze_new_posts(db, posts)
    return {"posts": len(posts), "analyses": len(analyses)}
