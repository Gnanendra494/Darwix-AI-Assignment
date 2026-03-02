import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.emotion import detect_emotion

def test_positive():
    label, intensity = detect_emotion("I love this!")
    assert label == "positive"
    assert intensity > 0

def test_negative():
    label, intensity = detect_emotion("This is terrible.")
    assert label == "negative"
    assert intensity > 0

def test_neutral():
    label, intensity = detect_emotion("It is a table.")
    assert label == "neutral"
    assert intensity == 0
