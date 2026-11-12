from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
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


def add_file_route(path, filename, media_type):
    def handler():
        return FileResponse(BASE / filename, media_type=media_type)
    app.add_api_route(path, handler, methods=["GET"], include_in_schema=False)


add_file_route("/", "index.html", "text/html")
for name, kind in [("sw.js", "application/javascript"),
                   ("manifest.json", "application/manifest+json"),
                   ("icon-192.png", "image/png"),
                   ("icon-512.png", "image/png")]:
    add_file_route("/" + name, name, kind)
    add_file_route("/static/" + name, name, kind)
