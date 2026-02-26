from pathlib import Path
import json
import os
from schemas import GenerateProjectTextOutput

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_ROOT / "src/outputs"


# ------------------------
# FILE OUTPUT STORAGE
# ------------------------

def save_generation(
    project_id: str,
    evaluation: dict,
    result: GenerateProjectTextOutput,
):
    # Ensure output directory exists
    BASE_DIR.mkdir(exist_ok=True)

    # Create project-specific directory
    project_dir = BASE_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

     # --- Save JSON (ground truth for evaluation) ---
    with (project_dir / "output.json").open("w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)

    with (project_dir / "evaluation.json").open("w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2, ensure_ascii=False)



