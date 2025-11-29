from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

from .base import TimestampMixin


class User(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="viewer")

    connectors: List["SocialConnector"] = Relationship(back_populates="creator")


class SocialConnector(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    name: str
    config: dict = Field(sa_column=Column(JSON))
    is_active: bool = True
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")

    creator: Optional[User] = Relationship(back_populates="connectors")
    posts: List["Post"] = Relationship(back_populates="connector")


class Post(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    connector_id: Optional[int] = Field(default=None, foreign_key="socialconnector.id")
    external_id: str
    source: str
    author_name: Optional[str] = None
    text: Optional[str] = None
    raw_text: Optional[str] = None
    language: Optional[str] = None
    published_at: Optional[datetime] = None
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    like_count: int = 0
    share_count: int = 0
    comment_count: int = 0
    url: Optional[str] = None

    connector: Optional[SocialConnector] = Relationship(back_populates="posts")
    analysis: Optional["PostAnalysis"] = Relationship(back_populates="post")
    categories: List["PostCategory"] = Relationship(back_populates="post")


class PostAnalysis(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    sentiment: str = "neutral"
    intent: str = "other"
    topics: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    keywords: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    is_flagged: bool = False

    post: Optional[Post] = Relationship(back_populates="analysis")
    category_links: List["PostCategory"] = Relationship(back_populates="analysis")


class Category(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    rules: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")

    posts: List["PostCategory"] = Relationship(back_populates="category")


class PostCategory(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    category_id: int = Field(foreign_key="category.id")

    post: Optional[Post] = Relationship(back_populates="categories")
    category: Optional[Category] = Relationship(back_populates="posts")
    analysis: Optional[PostAnalysis] = Relationship(back_populates="category_links")


class Recommendation(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    data: dict = Field(sa_column=Column(JSON))
    valid_until: Optional[datetime] = None


class Alert(TimestampMixin, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: str = "info"
    message: str
    data: dict = Field(default_factory=dict, sa_column=Column(JSON))
    is_seen: bool = False
