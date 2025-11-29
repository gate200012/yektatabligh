import re
from typing import List

POSITIVE = {"عالی", "خوب", "عاشق", "great", "love", "perfect"}
NEGATIVE = {"بد", "ضعیف", "نفرت", "hate", "terrible", "افتضاح"}


def normalize_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@[\w_]+", "", text)
    text = re.sub(r"#[\w_]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_language(text: str) -> str:
    if re.search(r"[آ-ی]", text):
        return "fa"
    if re.search(r"[a-zA-Z]", text):
        return "en"
    return "other"


def sentiment(text: str) -> str:
    tokens = set(text.split())
    if tokens & POSITIVE and not tokens & NEGATIVE:
        return "positive"
    if tokens & NEGATIVE and not tokens & POSITIVE:
        return "negative"
    if tokens & NEGATIVE and tokens & POSITIVE:
        return "neutral"
    return "neutral"


def intent(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ["?", "چطور", "کجا", "how", "what", "?"]):
        return "question"
    if any(word in lowered for word in ["شکایت", "بد", "hate", "افتضاح", "مشکل"]):
        return "complaint"
    if any(word in lowered for word in ["پیشنهاد", "should", "better"]):
        return "suggestion"
    if any(word in lowered for word in ["thanks", "مرسی", "love", "خوب"]):
        return "praise"
    return "other"


def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    tokens = [t for t in re.findall(r"\w+", text.lower()) if len(t) > 2]
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return [k for k, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:top_n]]


def match_categories(text: str, categories) -> List[int]:
    matches = []
    for category in categories:
        patterns = category.rules.get("keywords", []) if isinstance(category.rules, dict) else []
        if any(p.lower() in text.lower() for p in patterns):
            matches.append(category.id)
    return matches
