from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ConnectorBase(BaseModel):
    type: str
    name: str
    config: dict
    is_active: bool = True


class ConnectorCreate(ConnectorBase):
    pass


class ConnectorRead(ConnectorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    connector_id: int
    external_id: str
    source: str
    author_name: Optional[str]
    text: Optional[str]
    raw_text: Optional[str]
    language: Optional[str]
    published_at: Optional[datetime]
    like_count: int = 0
    share_count: int = 0
    comment_count: int = 0
    url: Optional[str]


class PostRead(PostBase):
    id: int
    collected_at: datetime

    class Config:
        orm_mode = True


class PostFilter(BaseModel):
    source: Optional[str] = None
    sentiment: Optional[str] = None
    intent: Optional[str] = None
    category_id: Optional[int] = None
    search: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rules: dict = {}


class CategoryRead(CategoryCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RecommendationRead(BaseModel):
    id: int
    type: str
    data: dict
    created_at: datetime
    valid_until: Optional[datetime]

    class Config:
        orm_mode = True


class AlertRead(BaseModel):
    id: int
    level: str
    message: str
    data: dict
    created_at: datetime
    is_seen: bool

    class Config:
        orm_mode = True
