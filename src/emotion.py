from typing import Tuple

# Try to use a Hugging Face emotion classifier when available. If not,
# fall back to the lightweight TextBlob polarity-based detector.
try:
    from transformers import pipeline

    _hf_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
except Exception:
    _hf_pipeline = None

try:
    from textblob import TextBlob
except Exception:
    TextBlob = None


def _map_hf_label_to_category(label: str) -> str:
    label = label.lower()
    if label in ("joy", "love", "relief", "positive"):
        return "positive"
    if label in ("anger", "sadness", "fear", "disgust", "negative"):
        return "negative"
    # surprise, neutral-like labels → neutral
    return "neutral"


def detect_emotion(text: str) -> Tuple[str, float]:
    """Return `(label, intensity)` where label ∈ {positive, negative, neutral}.

    If a Hugging Face model is available it will be used (more granular
    emotions are mapped into the three target buckets). Otherwise TextBlob is
    used as a fallback.  The `intensity` is a confidence-like value between
    0.0 and 1.0 (model score or absolute polarity).
    """
    if _hf_pipeline is not None:
        try:
            out = _hf_pipeline(text)
            if isinstance(out, list) and len(out) > 0:
                label = out[0]["label"]
                score = float(out[0].get("score", 0.0))
                category = _map_hf_label_to_category(label)
                return category, score
        except Exception:
            pass

    # fallback: TextBlob polarity
    if TextBlob is not None:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        intensity = min(1.0, max(0.0, abs(polarity)))
        if polarity > 0.1:
            return "positive", intensity
        if polarity < -0.1:
            return "negative", intensity
        return "neutral", 0.0

    # worst-case fallback
    return "neutral", 0.0
