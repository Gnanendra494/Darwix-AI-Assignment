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
    use_ssml: bool = False,
) -> str:
    """Generate speech from text using pyttsx3 and return output filename.

    The `intensity` parameter (0.0 – 1.0) scales how strongly the emotion
    affects rate and volume. `use_ssml` toggles a small SSML emulation layer
    (pyttsx3 does not support SSML natively, so emulation is performed).
    """
    engine = pyttsx3.init()
    # compute final properties
    delta = EMOTION_DELTA.get(emotion, EMOTION_DELTA["neutral"])
    rate = BASE_RATE + int(delta["rate"] * intensity)
    volume = max(0.0, min(1.0, BASE_VOLUME + delta["volume"] * intensity))

    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # Basic SSML emulation: transform <break/>, <emphasis>, <prosody> to simple
    # textual cues that the TTS engine can speak.
    if use_ssml:
        text = _emulate_ssml(text)

    tmp_output = filename
    # pyttsx3 writes in the "native" format; we'll write to an AIFF then
    # convert on platforms like macOS where the engine outputs AIFF data.
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


def _emulate_ssml(text: str) -> str:
    """Lightweight SSML emulation:

    - `<break time="500ms"/>` -> short pause (inserts ellipses)
    - `<emphasis>word</emphasis>` -> uppercase the word
    - `<prosody rate="fast">` -> append punctuation to increase energy
    """
    import re

    # break tags -> add dots proportional to time
    def _break_sub(m):
        ms = int(m.group(1)) if m.group(1) else 250
        dots = '.' * max(1, ms // 250)
        return ' ' + dots + ' '

    text = re.sub(r'<break[^>]*time="?(\d+)ms"?\s*/?>', _break_sub, text)
    # emphasis
    text = re.sub(r'<emphasis>(.*?)</emphasis>', lambda m: m.group(1).upper(), text)

    # simple prosody handling
    def _prosody_sub(m):
        attrs = m.group(1)
        inner = m.group(2)
        if 'rate="fast"' in attrs:
            return inner + '!!'
        return inner
    text = re.sub(r'<prosody([^>]*)>(.*?)</prosody>', _prosody_sub, text)
    return text
