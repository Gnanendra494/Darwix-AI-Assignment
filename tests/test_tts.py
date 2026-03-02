import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tts import synthesize_speech

def test_speech_output(tmp_path):
    text = "Hello world"
    emotion = "positive"
    intensity = 0.5
    filename = tmp_path / "test.wav"
    out = synthesize_speech(text, emotion, intensity, filename=str(filename))
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0
