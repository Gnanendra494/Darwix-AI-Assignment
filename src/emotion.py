from textblob import TextBlob
from typing import Tuple


def detect_emotion(text: str) -> Tuple[str, float]:
    """Analyze text and return a tuple `(label, intensity)`.

    I wanted a simple, explainable estimator so I picked TextBlob's polarity
    score; it’t easy to illustrate in the README and modify later if I decide to
    swap in a neural classifier.  The ``intensity`` lets the calling code know
    how "strong" the sentiment was, which lets the speech module exaggerate
    the effect.

    `label` is one of 'positive', 'negative', or 'neutral'.
    `intensity` is the absolute value of polarity (0.0–1.0) and can be used to
    scale vocal parameters.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    intensity = abs(polarity)
    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return label, intensity
