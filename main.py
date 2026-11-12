from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine import analyze

BASE = Path(__file__).parent
app = FastAPI(title="ScamShield")


class Msg(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


@app.post("/api/analyze")
def api_analyze(body: Msg):
    return analyze(body.message)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sw.js")
def service_worker():
    return FileResponse(BASE / "static" / "sw.js", media_type="application/javascript")


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")
