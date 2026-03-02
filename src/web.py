from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from emotion import detect_emotion
from tts import synthesize_speech

app = FastAPI()

HTML = """<!DOCTYPE html>
<html>
<head><title>Empathy Engine</title></head>
<body>
<h1>Empathy Engine</h1>
<form method="post" action="/speak">
  <textarea name="text" rows="4" cols="50"></textarea><br>
  <input type="submit" value="Speak">
</form>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML

@app.post("/speak")
def speak(text: str = Form(...)):
    emotion, intensity = detect_emotion(text)
    filename = synthesize_speech(text, emotion, intensity)
    return FileResponse(filename, media_type="audio/wav")
