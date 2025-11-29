from typing import List
from sqlmodel import Session

from app.models.models import Post, PostAnalysis, Category, PostCategory
from app.services import nlp


def analyze_post(session: Session, post: Post) -> PostAnalysis:
    text = post.text or post.raw_text or ""
    sentiment_value = nlp.sentiment(text)
    intent_value = nlp.intent(text)
    keywords = nlp.extract_keywords(text)

    analysis = PostAnalysis(
        post_id=post.id,
        sentiment=sentiment_value,
        intent=intent_value,
        keywords=keywords,
        topics=[],
        is_flagged=sentiment_value == "negative",
    )
    session.add(analysis)
    session.commit()
    session.refresh(analysis)

    categories = session.query(Category).all()
    category_ids = nlp.match_categories(text, categories)
    for cid in category_ids:
        link = PostCategory(post_id=post.id, category_id=cid)
        session.add(link)
    session.commit()
    return analysis


def analyze_new_posts(session: Session, posts: List[Post]) -> List[PostAnalysis]:
    analyses = []
    for post in posts:
        analyses.append(analyze_post(session, post))
    return analyses
