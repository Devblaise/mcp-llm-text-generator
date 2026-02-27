from mcp_app import mcp
from schemas import (GenerateProjectTextInput, GenerateProjectTextOutput, GeneratedText)
from context import build_context
from llm import generate_text_from_context
from resources import projects_resource
from evaluation import evaluate_generated_vs_reference
from utils import normalize_generated_entry, extract_keywords
from storage import save_generation, load_reference_text
import json
import logging

logging.basicConfig(level=logging.INFO)
#-------------------------
# TOOLS
#-------------------------
# Core tool to generate project texts and evaluate results
@mcp.tool()
async def generate_project_text(
    request: GenerateProjectTextInput,
    *,
    reference_text: str | None = None, 
    ) -> GenerateProjectTextOutput:
    """
    Generates both a detailed project page description and a short faculty teaser
    for a single research project.
    """
  
    logging.info(
        f"Generating text for project: {request.project_id} - {request.project_description[:50]}... "
        f"(languages={request.languages}, audience={request.target_audience})"
    )
    
    #--- Build LLM context ---
    logging.info("Building context prompt from project metadata...")
    prompt = build_context(request)
    logging.info(f"Context prompt built ({len(prompt)} characters). Invoking LLM...")
    
    #--- Invoke and Generate text via LLM (async) ---
    logging.info("Sending prompt to OpenAI API...")
    raw_response = await generate_text_from_context(prompt)
    logging.info(f"LLM response received ({len(raw_response)} characters).")
    
    try:
        logging.info("Parsing JSON response from LLM...")
        parsed= json.loads(raw_response)
        logging.info("JSON parsed successfully.")
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON response from LLM.")
        raise RuntimeError("LLM returned invalid JSON.") from e
    
    # --- Guardrails / validation checks ---
    #  Define required  sections
    required_sections = ["project_page", "faculty_teaser"]
    required_langs = [lang.value for lang in request.languages]  

    # Check sections exist
    missing_sections = [s for s in required_sections if s not in parsed]
    if missing_sections:
        raise RuntimeError(f"LLM response missing required sections: {', '.join(missing_sections)}")

    #  Check all requested languages are present in each section
    for section in required_sections:
        missing_langs = [lang for lang in required_langs if lang not in parsed.get(section, {})]
        if missing_langs:
            raise RuntimeError(f"LLM response missing languages {missing_langs} in {section}")
    
    # --- Normalize + parse project_page ---
    logging.info("Processing project page descriptions...")
    project_page = {}
    for lang, entry in parsed.get("project_page", {}).items():
        entry = normalize_generated_entry(entry)
        project_page[lang] = GeneratedText(**entry)
        logging.info(f" {lang.upper()}: {entry.get('word_count', 0)} words, "
                     f"{entry.get('reading_level', 'N/A')} level")
        
    # --- Normalize + parse faculty_teaser ---
    logging.info("Processing faculty teaser descriptions...")
    faculty_teaser = {}
    for lang, entry in parsed.get("faculty_teaser", {}).items():
        entry = normalize_generated_entry(entry)
        faculty_teaser[lang] = GeneratedText(**entry)
        logging.info(f" {lang.upper()}: {entry.get('word_count', 0)} words, "
                     f"{entry.get('reading_level', 'N/A')} level")
    
    #--- Creates the final output ---
    logging.info("Creating final output object...")
    result = GenerateProjectTextOutput(
        project_page=project_page,
        faculty_teaser=faculty_teaser,
        used_keywords=request.keywords,
        warnings=parsed.get("warnings"),
    )
    
    #--- Evaluation (optional) if reference text provided ---
    evaluation = None
    if reference_text:
        logging.info("Reference text provided. Running evaluation...")
        evaluation = evaluate_generated_vs_reference(
            project_id=request.project_id,
            generated_text=project_page["de"].text,
            human_reference_text=reference_text,
        )
        logging.info("Evaluation complete.")
        
    #--- Save outputs and evaluation ---
    logging.info("Saving generation results to storage...")
    save_generation(
        project_id=request.project_id,
        result=result,
        evaluation=evaluation,
    )
    logging.info(f"Generation complete for project {request.project_id}.")
    
    return result


# Adapter tool to generate project text from project ID
@mcp.tool()
async def generate_project_text_from_project_id(
    project_id: str,
) -> GenerateProjectTextOutput:
    """
    Adapter tool:
    - Reads project metadata from mcp://projects
    - Extracts semantic values
    - Loads reference text from src/data/references/{Abkürzung}.txt if exists
    - Calls generate_project_text with a proper request
    """
    projects = projects_resource()
    project = next(
        (p for p in projects if p["project_id"].lower() == project_id.lower()),
        None,
    )
    if not project:
        raise ValueError(f"Project not found: {project_id}")
    
    request = GenerateProjectTextInput(
        project_id=project["project_id"],
        project_description=project["Beschreibung"],
        keywords=extract_keywords(project),
        target_audience=["faculty", "industry"],
        languages=["de", "en"],
        source_type="excel", 
    )

    # Load reference text from storage
    reference_text = load_reference_text(project_id)
    if reference_text:
        logging.info(f"Loaded reference text for {project_id}")
    else:
        logging.info(f"No reference file found for {project_id} — evaluation will be skipped")
        

    return await generate_project_text(request, reference_text=reference_text)

