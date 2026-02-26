from mcp_app import mcp
import pandas as pd
import os

EXCEL_PATH = os.getenv("EXCEL_PATH", "src/data/2026-01-30_Projektbericht_öffentliche_Projekte.xlsx")


#-------------------------
# RESOURCES
#-------------------------

@mcp.resource("mcp://projects", mime_type="application/json")
def projects_resource():
    """
    Read-only project metadata loaded from Excel.
    """
    try:
        df = pd.read_excel(EXCEL_PATH)
    except FileNotFoundError:
        raise RuntimeError(f"Excel file not found: {EXCEL_PATH}")

    df.columns = [c.strip() for c in df.columns]

    # Add deterministic IDs if not present
    if "project_id" not in df.columns:
        df.insert(0, "project_id", [
            f"proj-{i:03d}" for i in range(1, len(df) + 1)
        ])

    return df.to_dict(orient="records")

