import sys
import argparse
from emotion import detect_emotion
from tts import synthesize_speech


def main():
    parser = argparse.ArgumentParser(description="Empathy Engine CLI")
    parser.add_argument('text', nargs='?', help='Text to speak')
    parser.add_argument('--ssml', action='store_true', help='Interpret input as SSML-like markup')
    args = parser.parse_args()

    if not args.text:
        print('Usage: python -m src.main "your text here" [--ssml]')
        sys.exit(1)

    text = args.text
    emotion, intensity = detect_emotion(text)
    print(f"Detected emotion: {emotion} (intensity={intensity:.2f})")
    filename = synthesize_speech(text, emotion, intensity, use_ssml=args.ssml)
    print(f"Audio written to {filename}")


if __name__ == "__main__":
    main()
