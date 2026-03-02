import sys
from emotion import detect_emotion
from tts import synthesize_speech


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main \"your text here\"")
        sys.exit(1)

    text = sys.argv[1]
    emotion, intensity = detect_emotion(text)
    print(f"Detected emotion: {emotion} (intensity={intensity:.2f})")
    filename = synthesize_speech(text, emotion, intensity)
    print(f"Audio written to {filename}")


if __name__ == "__main__":
    main()
