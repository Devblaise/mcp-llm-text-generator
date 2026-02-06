#**************************************
# Author: Mbadugha Kenechukwu
# Technichse Hoschule Köln (TH Köln)
# Communication Systems and Networks 
#*************************************

from mcp_app import mcp
from schemas import (GenerateProjectTextInput, GenerateProjectTextOutput, GeneratedText)
from context import build_context
from llm import generate_text_from_context
from resource import projects_resource
from evaluation import evaluate_generated_vs_reference
from utils import normalize_generated_entry
from storage import save_generation
import json
import logging

logging.basicConfig(level=logging.INFO)

#-------------------------
# TOOLS
#-------------------------

# Core tool to generate project texts and evaluate results
@mcp.tool()
def generate_project_text(
    request: GenerateProjectTextInput,
    *,
    reference_text: str | None = None,
    ) -> GenerateProjectTextOutput:
    """
    Generates both a detailed project page description and a short faculty teaser
    for a single research project.
    """
  
    logging.info(
        f"Generating text for project: {request.project_title}"
        f"(languages={request.languages}, audience={request.target_audience})"
    )
    
    #--- Build LLM context ---
    prompt = build_context(request)
    logging.info("Context built. Invoking LLM...")
    
    #--- Invoke and Generate text via LLM ---
    raw_response = generate_text_from_context(prompt)
    
    try:
        parsed= json.loads(raw_response)
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON response from LLM.")
        raise RuntimeError("LLM returned invalid JSON.") from e
    
    # --- Normalize + parse project_page ---
    project_page = {}
    for lang, entry in parsed["project_page"].items():
        entry = normalize_generated_entry(entry)
        project_page[lang] = GeneratedText(**entry)

    # --- Normalize + parse faculty_teaser ---
    faculty_teaser = {}
    for lang, entry in parsed["faculty_teaser"].items():
        entry = normalize_generated_entry(entry)
        faculty_teaser[lang] = GeneratedText(**entry)

    
    #--- Creates the final output ---
    result = GenerateProjectTextOutput(
        project_page=project_page,
        faculty_teaser=faculty_teaser,
        used_keywords=request.keywords,
        warnings=parsed.get("warnings"),
    )
    
    #--- Evaluation (optional) if reference text provided ---
    evaluation = None
    if reference_text:
        evaluation = evaluate_generated_vs_reference(
            project_id=request.project_id,
            generated_text=project_page["de"].text,
            reference_text=reference_text,
        )
        
    #--- Save outputs and evaluation ---
    save_generation(
        project_id=request.project_id,
        result=result,
        evaluation=evaluation,
    )
    
    return result

# Adapter tool to generate project text from project ID
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

    projects = projects_resource()

    project = next(
        (p for p in projects if p["project_id"] == project_id),
        None,
    )
    if not project:
        raise ValueError(f"Project not found: {project_id}")

    # extract VALUES from excel sheet ----
    keywords = []
    for kw in[
        project.get("Mittelgeber"),
        project.get("Drittmittelgeberkategorie"),
		project.get("Kooperationspartner"),
        project.get("Mittelherkunft"),
		project.get("Projektzweck")
    ]:
        if isinstance(kw, str):
            keywords.extend(p.strip() for p in kw.replace(",", ";").split(";") if p.strip())

    request = GenerateProjectTextInput(
        project_id=project["project_id"],
        project_title=project["Projekttitel"],
        keywords=keywords,
        target_audience=["faculty", "industry"],
        languages=["de", "en"],
        source_type="excel", 
    )
    reference_text=project.get("Beschreibung")

    return generate_project_text(request, reference_text=reference_text)

