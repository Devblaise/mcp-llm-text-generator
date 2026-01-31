import pandas as pd
from schemas import ProjectTextGenerationRequest
from typing import List
from server import generate_project_text


EXCEL_FILE_PATH = "src/data/2026-01-30_Projektbericht_öffentliche_Projekte.xlsx"

df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="Tabelle1")

def row_to_request(row) -> ProjectTextGenerationRequest:
    # Title
    project_title = str(row["Projekttitel"]).strip()

    # Research field (fallback logic)
    research_field = (
        str(row.get("Organisationseinheiten der Projektleitungen", "")).strip()
        or str(row.get("Koordinierende Institution", "")).strip()
        or "Research Project"
    )

    # Keywords (aggregated, non-technical)
    keyword_sources = [
        "Abkürzung",
        "Kooperationspartner",
        "Mittelgeber",
        "Drittmittelgeberkategorie",
        "Projektmitglieder",
    ]

    keywords: List[str] = []
    for col in keyword_sources:
        if col in row and pd.notna(row[col]):
            parts = str(row[col]).replace(";", ",").split(",")
            keywords.extend(p.strip() for p in parts if p.strip())

    # Deduplicate keywords
    keywords = list(dict.fromkeys(keywords))[:12]

    return ProjectTextGenerationRequest(
        project_title=str(row["Projekttitel"]),
        keywords=[
            str(row.get("Mittelgeber", "")),
            str(row.get("Kooperationspartner", ""))
        ],
        target_audience=["faculty", "industry"],
        languages=["en", "de"],
        source_type="excel"
    )

def run_batch(limit: int = 5):
    results = []

    for _, row in df.head(limit).iterrows():
        request = row_to_request(row)
        result = generate_project_text(request)
        results.append({
            "project_title": request.project_title,
            "result": result.model_dump()
        })

    return results

if __name__ == "__main__":
   outputs = run_batch(limit=5)
   print(outputs[0])
