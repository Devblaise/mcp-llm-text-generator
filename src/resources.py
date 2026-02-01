import pandas as pd
import uuid

EXCEL_PATH = "src/data/2026-01-30_Projektbericht_öffentliche_Projekte.xlsx"

def load_excel_projects():
    df = pd.read_excel(EXCEL_PATH)
    df.columns = [c.strip() for c in df.columns]

    # Add deterministic IDs if not present
    if "project_id" not in df.columns:
        df.insert(0, "project_id", [
            f"proj-{i:04d}" for i in range(len(df))
        ])

    return df.to_dict(orient="records")

