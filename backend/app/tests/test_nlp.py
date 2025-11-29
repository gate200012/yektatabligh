from app.services import nlp


def test_sentiment_positive():
    assert nlp.sentiment("این محصول عالی است") == "positive"


def test_detect_language_fa():
    assert nlp.detect_language("سلام") == "fa"
