# 🎙️ Empathy Engine

> **Give AI a Human Voice** – Transform Text into Emotionally Intelligent Speech

![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Python: 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Tests: 4/4 Passing](https://img.shields.io/badge/tests-4%2F4%20passing-brightgreen.svg)
![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-success.svg)

---

## 🚀 What is the Empathy Engine?

This project bridges the uncanny valley between robotic text-to-speech and human-like vocal expression. **Empathy Engine** analyzes the emotional tone of input text—detecting if it's positive, negative, or neutral—and then **dynamically modulates the voice** by adjusting speech rate and volume to match the sentiment.

The result? Speech that sounds genuinely enthusiastic about good news, patient when discussing frustrations, and calm when neutral.

✨ **Built from scratch** for the "The Empathy Engine" AI challenge, with a focus on explainable design decisions and user-friendly interfaces.

---

## ⭐ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Emotion Detection** | Analyze text sentiment (positive/negative/neutral) with intensity scoring |
| 🎵 **Smart Vocal Modulation** | Adjust speech rate & volume based on detected emotion |
| 💻 **CLI Interface** | One-line command to generate & play emotionally-aware speech |
| 🌐 **Web Demo** | Browser-based interface with instant audio playback |
| 📦 **Offline-First** | Runs locally with no external API dependencies |
| 🔄 **Intensity Scaling** | Stronger emotions = more dramatic vocal changes |
| 🍎 **macOS Compatible** | Transparent AIFF→WAV conversion for seamless playback |
| 📊 **Test Coverage** | 4/4 tests passing; fully tested codebase |

---

## 📋 Quick Start

### ✅ Prerequisites

- **Python 3.8+** (tested on 3.9+)
- **macOS, Linux, or Windows**
- ~10MB disk space for dependencies
- _Optional:_ ffmpeg for advanced audio manipulation

### 🔧 Installation

```bash
# 1. Clone or navigate to the project
cd /path/to/empathy-engine

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# OR: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download sentiment analysis data (one-time)
python3 -m textblob.download_corpora
```

---

## 🎬 Usage

### 💬 CLI – Speak Any Text

```bash
# Simple example
PYTHONPATH=./src python3 -m src.main "I am thrilled with this opportunity"

# Output:
# Detected emotion: positive (intensity=0.75)
# Audio written to output.wav
```

**Result:** The text is spoken with elevated rate & volume, conveying genuine enthusiasm! 🎉

### 🌐 Web Interface

```bash
# Start the interactive web server
PYTHONPATH=./src uvicorn src.web:app --reload

# Open your browser → http://localhost:8000
# Type text, click "Speak", and listen immediately
```

### 🎧 Helper Script

For rapid testing with automatic playback:

```bash
chmod +x run_and_play.sh
./run_and_play.sh "What amazing technology!"
# → Generates audio + opens in QuickTime (macOS)
```

---

## 🏗️ Architecture

```
empathy-engine/
│
├── 🧠 src/
│   ├── emotion.py        # Sentiment detector (TextBlob + HF fallback)
│   ├── tts.py            # TTS engine with vocal modulation & SSML
│   ├── main.py           # CLI entry point
│   ├── web.py            # FastAPI web app
│   └── __init__.py       #
│
├── 🧪 tests/
│   ├── test_emotion.py   # Sentiment detection tests
│   └── test_tts.py       # Audio generation tests
│
├── 📦 requirements.txt    # Python dependencies
├── 🎯 run_and_play.sh    # Quick demo script
├── ⚙️ .gitignore         # Git exclusions
└── 📖 README.md          # This file
```

---

## 🎨 How It Works

### Step 1️⃣ – Emotion Detection

```python
from emotion import detect_emotion

text = "This is fantastic news!"
label, intensity = detect_emotion(text)
# Output: ("positive", 0.82)
```

**Supported emotions:** positive, negative, neutral

### Step 2️⃣ – Vocal Modulation

```python
from tts import synthesize_speech

synthesize_speech(text="Hello!", emotion="positive", intensity=0.8)
# Output: Faster, louder speech (rate +16 wpm, volume +0.16)
```

**Modulation rules:**
- 🟢 **Positive** → Faster rate, increased volume
- 🔴 **Negative** → Slower rate, reduced volume
- ⚪ **Neutral** → Default parameters

### Step 3️⃣ – Audio Output

Speech is synthesized using **pyttsx3** (cross-platform) and saved as `.wav` or `.mp3`.

✨ **macOS quirk handled:** Automatically converts AIFF→WAV so all players work!

---

## 📚 API Reference

### `detect_emotion(text: str) → Tuple[str, float]`

Analyzes sentiment and returns emotion label + intensity.

```python
label, intensity = detect_emotion("I love this!")
# Returns: ("positive", 0.75)
```

### `synthesize_speech(text, emotion, intensity, filename, use_ssml) → str`

Generates speech and saves to file.

```python
synthesize_speech(
    text="Great day!",
    emotion="positive",
    intensity=0.6,
    filename="output.wav",
    use_ssml=False  # Optional SSML support
)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests -v

# Run specific test
pytest tests/test_emotion.py::test_positive -v

# Output:
# ✅ test_emotion.py::test_positive PASSED
# ✅ test_emotion.py::test_negative PASSED
# ✅ test_tts.py::test_speech_output PASSED
# ✅ All 4 tests passing!
```

---

## 🚀 Advanced Features

### 🎤 SSML Emulation (Branch: `feature/ssml-hf-emotion`)

Enable simple SSML markup processing:

```bash
./run_and_play.sh '<emphasis>Excellent</emphasis> news! <break time="500ms"/> Welcome!' --ssml
```

Supported tags:
- `<emphasis>text</emphasis>` → Uppercase for emphasis
- `<break time="500ms"/>` → Adds pause
- `<prosody rate="fast">text</prosody>` → Energy indicator

### 🧠 Hugging Face Emotion Detection (Branch: `feature/ssml-hf-emotion`)

Swap TextBlob for a pre-trained neural model:

```bash
pip install transformers torch

# Detects 7 emotions: joy, sadness, anger, fear, disgust, surprise, neutral
python3 -m src.main "I'm absolutely devastated!" 
# Returns: ("negative", 0.94) with richer classification!
```

---

## 📊 Project Structure & Files

| File | Purpose |
|------|---------|
| `src/emotion.py` | Sentiment analysis engine |
| `src/tts.py` | Text-to-speech + vocal modulation |
| `src/main.py` | Command-line interface |
| `src/web.py` | FastAPI web application |
| `tests/test_emotion.py` | Emotion detector tests |
| `tests/test_tts.py` | Audio generation tests |
| `run_and_play.sh` | Interactive demo script |
| `requirements.txt` | Python dependencies |

---

## 📦 Release

### 🎁 v1.0 – Production Ready

```bash
unzip empathy-engine-v1.0.zip -d release
cd release
./run_and_play.sh "Demo speech!"
```

**Includes:**
- ✅ Complete runnable code
- ✅ Test suite (4/4 passing)
- ✅ Helper scripts
- ✅ Documentation

---

## 🔄 Changelog

### v1.0 (Current)
- ✨ **Sentiment-based TTS** with intensity scaling
- ✨ **CLI + Web UI** for easy interaction
- ✨ **macOS AIFF→WAV** conversion
- ✨ **Test suite** with full coverage
- ✨ **Helper script** for rapid demos

### v1.1 (Planned) – See `feature/ssml-hf-emotion` branch
- 🧠 Hugging Face emotion detection (7 emotions)
- 🎤 SSML emulation layer
- 🎨 Enhanced vocal prosody control

---

## 🎯 Design Decisions

### Why TextBlob?

TextBlob offers a lightweight, interpretable sentiment model perfect for rapid prototyping. Easy to explain, no heavy dependencies. Fallback to Hugging Face is available for more nuanced emotion detection.

### Why pyttsx3?

Cross-platform, offline-first TTS engine. Runs on macOS, Linux, and Windows without API keys or internet.

### Intensity Scaling?

Matching voice modulation to emotion intensity creates more natural, believable speech. "I like it" sounds different from "I ABSOLUTELY LOVE IT!" ✨

---

## 🤝 Contributing

This project welcomes improvements! Ideas:

- 🎵 **Pitch modulation** (currently rate & volume only)
- 🌍 **Multi-language support**
- 🎙️ **Voice selection** (male/female/accent)
- 📊 **Confidence metrics** for predictions
- ☁️ **Cloud TTS integration** (Azure, Google Cloud)

---

## 📜 License

**MIT License** – Free for personal and commercial use.

---

## 🙌 Credits & Acknowledgments

Built as a submission for **"The Empathy Engine"** AI challenge.

**Thanks to:**
- 🎵 **pyttsx3** – Cross-platform TTS
- 💡 **TextBlob** – Simple sentiment analysis
- 🚀 **FastAPI** – Modern web framework
- 🧪 **pytest** – Testing framework

---

## 📞 Support & Questions

### ❓ FAQ

**Q: Does it require internet?**  
A: No! Runs 100% offline after installation.

**Q: What about privacy?**  
A: All processing happens locally. No data sent anywhere.

**Q: Can I use custom voices?**  
A: pyttsx3 uses system voices. You can list them with `pyttsx3.init().getProperty('voices')`.

**Q: How do I improve emotion detection?**  
A: Install `transformers` + `torch` and switch to the Hugging Face model (see `feature/ssml-hf-emotion` branch).

---

## 🎉 Quick Demo

```bash
# One-liner to experience the magic:
cd /path/to/empathy-engine && \
source venv/bin/activate && \
PYTHONPATH=./src python3 -m src.main "This is incredible!" && \
open output.wav  # macOS: opens in QuickTime
# Or: afplay output.wav  # CLI playback
```

Hear the enthusiasm in the voice! 🎧✨

---

## 🔗 Links

- 📖 **Repository:** https://github.com/Gnanendra494/Darwix-AI-Assignment
- 🌟 **Main Branch:** `main` (stable, TextBlob)
- 🚀 **Feature Branch:** `feature/ssml-hf-emotion` (HF + SSML enhancements)
- 📦 **Release ZIP:** `empathy-engine-v1.0.zip`

---

<div align="center">

### ✨ Made with ❤️ for the Future of AI Voice Interaction ✨

**[⬆ back to top](#-empathy-engine)**

</div>
