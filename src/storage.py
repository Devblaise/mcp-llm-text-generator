from pathlib import Path
import json
import os
from schemas import GenerateProjectTextOutput

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = Path(os.getenv("OUTPUT_DIR", PROJECT_ROOT / "src/outputs"))
REFERENCES_DIR = Path(__file__).parent / "data" / "references"


# ------------------------
# FILE INPUT/OUTPUT STORAGE
# ------------------------

def load_reference_text(project_id: str) -> str | None:
    """
    Load human-written reference text for evaluation.
    Looks for: src/data/references/{project_id}.txt
    Returns None if file doesn't exist.
    """
    reference_file = REFERENCES_DIR / f"{project_id}.txt"
    if reference_file.exists():
        return reference_file.read_text(encoding="utf-8").strip()
    return None


def save_generation(
    project_id: str,
    result: GenerateProjectTextOutput,
    evaluation: dict | None = None,
):
    # Ensure output directory exists
    BASE_DIR.mkdir(exist_ok=True)

    # Create project-specific directory
    project_dir = BASE_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    # --- Save JSON (ground truth for evaluation) ---
    with (project_dir / "output.json").open("w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)

    # --- Save evaluation results if provided ---
    if evaluation:
        with (project_dir / "evaluation.json").open("w", encoding="utf-8") as f:
            json.dump(evaluation, f, indent=2, ensure_ascii=False)



