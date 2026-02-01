from pathlib import Path
import json
import os
from schemas import GenerateProjectTextOutput

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_ROOT / "outputs"

def save_generation(
    project_id: str,
    result: GenerateProjectTextOutput,
):
    # Ensure output directory exists
    BASE_DIR.mkdir(exist_ok=True)

    # Create project-specific directory
    project_dir = BASE_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    with (project_dir / "output.json").open("w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)

    for lang, page in result.project_page.items():
        (project_dir / f"project_page_{lang}.txt").write_text(
            page.text, encoding="utf-8"
        )

    for lang, teaser in result.faculty_teaser.items():
        (project_dir / f"faculty_teaser_{lang}.txt").write_text(
            teaser.text, encoding="utf-8"
        )
