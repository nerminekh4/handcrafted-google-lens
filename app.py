from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import os
import shutil

from backend import ImageAgent

app = FastAPI(title="Handcrafted Google Lens")

app.mount("/static", StaticFiles(directory="static"), name="static")

agent = ImageAgent()


@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    if suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        suffix = ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        description = agent.ask_vision_model(image_path=tmp_path)
    except Exception as e:
        description = f"Erreur lors de l'analyse : {str(e)}"
    finally:
        os.unlink(tmp_path)

    # Return an HTML fragment — HTMX will swap it into #result
    safe_description = description.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lines = safe_description.split("\n")
    paragraphs = "".join(f"<p>{line}</p>" for line in lines if line.strip())

    return f"""
<div class="result-card">
  <div class="result-icon">🔍</div>
  <div class="result-text">{paragraphs}</div>
</div>
"""
