# Empathy Engine

This project was built from scratch as part of the AI challenge "The Empathy Engine". I wanted a lightweight Python tool that
could take a string, figure out how it was feeling, and then have a voice say it the "right" way. It's intentionally simple,
using TextBlob for sentiment so I could focus on the audio behaviour rather than training models.  The engine listens for
positive/negative/neutral cues and adjusts rate and volume so the result feels a little less robotic and a little more like a
person having a reaction.

Below you’ll find instructions on how to run it, what decisions I made during development, and how you can extend it.

## Features
- CLI and optional web interface (FastAPI) for text input
- Emotion detection using TextBlob
- TTS generation using pyttsx3 with rate and volume modulation
- Audio output saved as `.mp3` or `.wav`

## Getting Started

### Prerequisites
- Python 3.8+

### Installation
```bash
cd "${YOUR_WORKSPACE}/empathy-engine"
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Usage

#### Prerequisite Step
TextBlob requires some NLTK corpora for sentiment analysis. After installing packages run:

```bash
python -m textblob.download_corpora
```

#### CLI
```bash
python -m src.main "Your text here"
```
The generated file will be saved to `output.wav` (or `output.mp3` if you prefer).

> **macOS note:** the speech engine often writes compressed AIFF data even when
> you request a `.wav` file.  Most media players ignore it, giving the illusion
> of silence.  The code now transparently converts AIFF to WAV/MP3 so you should
> always get a playable file.  If you still see `output.wav` but no sound, open
> it in QuickTime to verify the content or try `ffplay output.wav`.

### Running Tests

Make sure `pytest` is installed (included in `requirements.txt`). Then run:

```bash
pytest tests
```

#### Web Interface (optional)
```bash
# install extra dependency for form handling
pip install python-multipart
# start server (ensure PYTHONPATH if running from root)
PYTHONPATH=./src uvicorn src.web:app --reload
```
Open http://localhost:8000 in your browser, type text, and listen to the response.

## Design Notes
- Sentiment is mapped to rate and volume via a simple dictionary.
  The analysis returns both a label and an intensity score (0.0–1.0),
  allowing **intensity scaling**: stronger emotions produce greater changes.
  - **Positive**: faster / louder (scale with intensity)
  - **Negative**: slower / quieter (scale with intensity)
  - **Neutral**: default parameters
- pyttsx3 is used for offline TTS; rate and volume can be changed programmatically.
- Bonus features implemented:
  - Intensity scaling based on sentiment polarity magnitude
  - Test suite covers the new tuple output
- Future improvements could include granular emotion categories (angry,
  surprised, etc.), SSML support, or a richer web UI.

## License
MIT
