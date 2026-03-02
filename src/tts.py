import pyttsx3

# base settings
# I chose 150 words per minute because it sounded close to a natural speaking pace
BASE_RATE = 150
BASE_VOLUME = 1.0

# base adjustments for each emotion (will be scaled by intensity)
# these deltas come from a bit of trial-and-error listening; positive should be
# a touch faster and louder, negative a bit slower/quieter.
EMOTION_DELTA = {
    "positive": {"rate": 20, "volume": 0.2},
    "negative": {"rate": -20, "volume": -0.3},
    "neutral": {"rate": 0, "volume": 0},
}


def synthesize_speech(
    text: str,
    emotion: str,
    intensity: float = 0.0,
    filename: str = "output.wav",
) -> str:
    """Generate speech from text using pyttsx3 and return output filename.

    The `intensity` parameter (0.0 – 1.0) scales how strongly the emotion
    affects rate and volume. A highly positive sentence will speak faster and
    louder than a mildly positive one.

    On macOS the pyttsx3 driver produces AIFF files even when given a .wav
    extension, which most players don't auto-detect. We therefore convert the
    result using pydub if the desired extension is .wav or .mp3.
    """
    engine = pyttsx3.init()
    # compute final properties
    delta = EMOTION_DELTA.get(emotion, EMOTION_DELTA["neutral"])
    rate = BASE_RATE + int(delta["rate"] * intensity)
    volume = max(0.0, min(1.0, BASE_VOLUME + delta["volume"] * intensity))

    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    tmp_output = filename
    # pyttsx3 writes in the "native" format; we'll always write to a temp file
    # and then convert if necessary.
    if filename.lower().endswith(('.wav', '.mp3')):
        tmp_output = filename + '.aiff'
    engine.save_to_file(text, tmp_output)
    engine.runAndWait()

    # convert if needed
    if tmp_output != filename:
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(tmp_output)
            audio.export(filename, format=filename.rsplit('.',1)[-1])
        except Exception:
            # conversion failed, just keep the raw file and rename
            import os
            os.replace(tmp_output, filename)
    return filename
