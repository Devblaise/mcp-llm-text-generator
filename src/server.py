from mcp.server.fastmcp import FastMCP
from schemas import (GenerateProjectTextInput, GenerateProjectTextOutput, GeneratedText)
from context import build_context
from llm import generate_text_from_context
from resources import load_excel_projects
from storage import save_generation
import json
import logging

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("project-text-generator")

#-------------------------
# RESOURCES
#-------------------------
@mcp.resource("mcp://projects", mime_type="application/json")
def projects_resource():
    """
    Read-only project metadata loaded from Excel.
    """
    return load_excel_projects()


#-------------------------
# TOOLS
#-------------------------
@mcp.tool()
def generate_project_text(
    request: GenerateProjectTextInput,
    ) -> GenerateProjectTextOutput:
    """
    Generates both a detailed project page description and a short faculty teaser
    for a single research project.
    """
  
    logging.info(
        f"Generating text for project: {request.project_title}",
        f"(languages={request.languages}, audience={request.target_audience})"
    )
    
    #--- Build LLM context ---
    prompt = build_context(request)
    logging.info("Context built. Invoking LLM...")
    raw_response = generate_text_from_context(prompt)
    
    try:
        parsed= json.loads(raw_response)
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON response from LLM.")
        raise RuntimeError("LLM returned invalid JSON.") from e
    
    #--- Parsed outputs ---
    project_page = {
        lang: GeneratedText(**entry)
        for lang, entry in parsed["project_page"].items()
    }
    faculty_teaser = {
        lang: GeneratedText(**entry)
        for lang, entry in parsed["faculty_teaser"].items()
    }
    warnings = parsed.get("warnings") or []
    
    result = GenerateProjectTextOutput(
        project_page=project_page,
        faculty_teaser=faculty_teaser,
        used_keywords=request.keywords,
        warnings=warnings or None,
    )

    # persist output
    save_generation(
        project_id=request.project_id,
        result=result,
    )

    return result

    
@mcp.tool()
def generate_project_text_from_project_id(
    project_id: str,
) -> GenerateProjectTextOutput:
    """
    Adapter tool:
    - Reads project metadata from mcp://projects
    - Extracts semantic values
    - Calls generate_project_text with a proper request
    """

    projects = load_excel_projects()

    project = next(
        (p for p in projects if p["project_id"] == project_id),
        None,
    )
    if not project:
        raise ValueError(f"Project not found: {project_id}")

    # extract VALUES from excel sheet ----
    raw_keywords = [
        project.get("Mittelgeber"),
        project.get("Drittmittelgeberkategorie"),
        project.get("Forschungsfelder"),
		project.get("Kooperationspartner"),
        project.get("Mittelherkunft"),
		project.get("Projektzweck")
    ]

    keywords = []
    for kw in raw_keywords:
        if isinstance(kw, str) and kw.strip():
            keywords.extend(
                part.strip()
                for part in kw.replace(",", ";").split(";")
                if part.strip()
            )

    request = GenerateProjectTextInput(
        project_id=project["project_id"],
        project_title=project["Projekttitel"],
        keywords=keywords,
        target_audience=["faculty", "industry"],
        languages=["en", "de"],
        source_type="excel",
    )

    return generate_project_text(request)


if __name__ == "__main__":
    mcp.run()
