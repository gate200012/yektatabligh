from datetime import datetime
from typing import List
from sqlmodel import Session

from app.models.models import SocialConnector, Post
from app.services import nlp


class ConnectorClient:
    def fetch_posts(self, connector: SocialConnector) -> List[dict]:
        raise NotImplementedError


class TwitterClient(ConnectorClient):
    def fetch_posts(self, connector: SocialConnector) -> List[dict]:
        # Demo/mock implementation
        keywords = connector.config.get("keywords", ["brand"])
        now = datetime.utcnow()
        return [
            {
                "external_id": f"tw-{i}",
                "source": "twitter",
                "author_name": "demo_user",
                "text": f"{kw} عالی است" if i % 2 == 0 else f"{kw} بد است",
                "raw_text": f"{kw} خام",
                "language": "fa",
                "published_at": now,
                "like_count": i * 2,
                "share_count": i,
                "comment_count": i,
                "url": "https://twitter.com/demo",
            }
            for i, kw in enumerate(keywords)
        ]


class TelegramClient(ConnectorClient):
    def fetch_posts(self, connector: SocialConnector) -> List[dict]:
        channels = connector.config.get("channels", ["demo"])
        now = datetime.utcnow()
        return [
            {
                "external_id": f"tg-{i}",
                "source": "telegram",
                "author_name": channel,
                "text": f"پیام جدید از {channel}",
                "raw_text": f"پیام جدید از {channel}",
                "language": "fa",
                "published_at": now,
                "like_count": 0,
                "share_count": 0,
                "comment_count": 0,
                "url": "https://t.me/demo",
            }
            for i, channel in enumerate(channels)
        ]


CLIENTS = {
    "twitter": TwitterClient(),
    "telegram": TelegramClient(),
}


def ingest_connector(session: Session, connector: SocialConnector) -> List[Post]:
    client = CLIENTS.get(connector.type)
    if not client:
        return []
    posts: List[Post] = []
    for payload in client.fetch_posts(connector):
        normalized_text = nlp.normalize_text(payload.get("text", ""))
        language = nlp.detect_language(payload.get("text", ""))
        post = Post(
            connector_id=connector.id,
            external_id=payload["external_id"],
            source=payload["source"],
            author_name=payload.get("author_name"),
            text=normalized_text,
            raw_text=payload.get("text"),
            language=language,
            published_at=payload.get("published_at"),
            like_count=payload.get("like_count", 0),
            share_count=payload.get("share_count", 0),
            comment_count=payload.get("comment_count", 0),
            url=payload.get("url"),
        )
        posts.append(post)
        session.add(post)
    session.commit()
    return posts
