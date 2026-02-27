from mcp_app import mcp
import pandas as pd
import os
import stat

EXCEL_PATH = os.getenv("EXCEL_PATH", "src/data/2026-01-30_Projektbericht_öffentliche_Projekte.xlsx")


#-------------------------
# RESOURCES
#-------------------------

# Helper function to set file permissions to read-only
def _ensure_read_only(path: str):
    """Set file permissions to read-only (owner/group/others)."""
    current = os.stat(path).st_mode
    read_only = current & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    if current != read_only:
        os.chmod(path, read_only)


@mcp.resource("mcp://projects", mime_type="application/json")
def projects_resource():
    """
    Read-only project metadata loaded from Excel.
    """
    try:
        _ensure_read_only(EXCEL_PATH)
        df = pd.read_excel(EXCEL_PATH)
    except FileNotFoundError:
        raise RuntimeError(f"Excel file not found: {EXCEL_PATH}")

    df.columns = [c.strip() for c in df.columns]

    # Use 'Abkürzung' (abbreviation) as the unique project identifier
    if "Abkürzung" not in df.columns:
        raise RuntimeError("Excel file missing required column: 'Abkürzung'")

    df.insert(0, "project_id", df["Abkürzung"].astype(str).str.strip())

    return df.to_dict(orient="records")

