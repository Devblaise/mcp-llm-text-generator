from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import functools
from pathlib import Path
import json

# ─── Configuration ───────────────────────────────────────────

OUTPUTS_DIR = Path(__file__).parent / "src" / "outputs"
REFERENCES_DIR = Path(__file__).parent / "src" / "data" / "references"

app = FastAPI(
    title="MCP Text Generator",
    description="Dashboard for viewing generated university project texts",
    version="0.1.0",
)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


# ─── Helper functions ────────────────────────────────────────

def get_projects() -> list[str]:
    if not OUTPUTS_DIR.exists():
        return []
    return sorted(
        p.name for p in OUTPUTS_DIR.iterdir()
        if p.is_dir() and (p / "output.json").exists()
    )


def load_json(path: Path) -> dict | None:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def load_text(path: Path) -> str | None:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return None


@functools.lru_cache(maxsize=128)
def _parse_text_blocks(text: str) -> list[dict]:
    """Convert raw generated text into a list of rendering blocks.

    Blocks have shape:
      - {'type': 'header', 'lead': 'First', 'rest': 'Remaining', 'body': 'optional body'}
      - {'type': 'para', 'text': '...'}
    """
    if not text:
        return []
    blocks: list[dict] = []
    # split by empty line groups
    parts = [p for p in text.split('\n\n') if p.strip()]
    for part in parts:
        s = part.strip()
        if s.startswith('### '):
            content = s[4:]
            if '\n' in content:
                header_line, body = content.split('\n', 1)
            else:
                header_line, body = content, ''
            header_line = header_line.strip()
            if ' ' in header_line:
                first, rest = header_line.split(' ', 1)
            else:
                first, rest = header_line, ''
            blocks.append({'type': 'header', 'lead': first, 'rest': rest, 'body': body.strip()})
        else:
            blocks.append({'type': 'para', 'text': s.replace('\n', ' ')})
    return blocks


# ─── API Routes ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    projects = get_projects()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projects": projects,
    })


@app.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    output = load_json(OUTPUTS_DIR / project_id / "output.json")
    evaluation = load_json(OUTPUTS_DIR / project_id / "evaluation.json")
    reference = load_text(REFERENCES_DIR / f"{project_id}.txt")

    if not output:
        return HTMLResponse(content="Project not found", status_code=404)

    # Preprocess project_page texts into rendering blocks so templates stay presentation-only
    project_page_blocks = {}
    if output.get('project_page'):
        for lang, entry in output['project_page'].items():
            text = entry.get('text', '') if isinstance(entry, dict) else (entry or '')
            project_page_blocks[lang] = _parse_text_blocks(text)

    return templates.TemplateResponse("project.html", {
        "request": request,
        "project_id": project_id,
        "output": output,
        "project_page_blocks": project_page_blocks,
        "evaluation": evaluation,
        "reference": reference,
        "projects": get_projects(),
    })


@app.get("/api/project/{project_id}/output")
async def download_output(project_id: str):
    data = load_json(OUTPUTS_DIR / project_id / "output.json")
    if not data:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return JSONResponse(
        content=data,
        headers={"Content-Disposition": f'attachment; filename="{project_id}_output.json"'},
    )


@app.get("/api/project/{project_id}/evaluation")
async def download_evaluation(project_id: str):
    data = load_json(OUTPUTS_DIR / project_id / "evaluation.json")
    if not data:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return JSONResponse(
        content=data,
        headers={"Content-Disposition": f'attachment; filename="{project_id}_evaluation.json"'},
    )


@app.get("/api/project/{project_id}/reference")
async def download_reference(project_id: str):
    text = load_text(REFERENCES_DIR / f"{project_id}.txt")
    if not text:
        return PlainTextResponse("Not found", status_code=404)
    return PlainTextResponse(
        content=text,
        headers={"Content-Disposition": f'attachment; filename="{project_id}_reference.txt"'},
    )
