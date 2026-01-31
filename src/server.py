from mcp.server.fastmcp import FastMCP
from schemas import (ProjectTextGenerationRequest, ProjectTextGenerationResult, GeneratedText, ReadingLevel)
from context import build_context
from llm import generate_text_from_context
import json
import logging

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("project-text-generator")


@mcp.tool()
def generate_project_text(
    request: ProjectTextGenerationRequest,
    ) -> ProjectTextGenerationResult:
    """
    Generates both a detailed project page description and a short faculty teaser
    from sparse project metadata using a single LLM call.
    """
    
    logging.info(f"Received request for project: {request.project_title} Building LLM context...")
    prompt = build_context(request)
    
    logging.info("Context built. Invoking LLM...")
    raw_response = generate_text_from_context(prompt)
    logging.info("LLM response received. Parsing output...")
    
    try:
        parsed= json.loads(raw_response)
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON response from LLM.")
        raise RuntimeError("LLM returned invalid JSON.") from e
    
    #--- Parse project page ---
    project_page = {}
    
    for lang_code, entry in parsed["project_page"].items():
        project_page[lang_code] = GeneratedText(
            text=entry.get("text", ""),
            reading_level=entry.get("reading_level"),
            word_count=entry.get("word_count", 0),
        )

    #--- Parse faculty teaser ---
    faculty_teaser = {}
    
    for lang_code, entry in parsed["faculty_teaser"].items():
        faculty_teaser[lang_code] = GeneratedText(
            text=entry.get("text", ""),
            reading_level=entry.get("reading_level"),
            word_count=entry.get("word_count", 0),
        )
    
    warnings = parsed.get("warnings") or []

    pp_len = sum(page.word_count for page in project_page.values())
    ft_len = sum(teaser.word_count for teaser in faculty_teaser.values())

    if not 300 <= pp_len <= 500:
        warnings.append(
            f"Project page length ({pp_len} words) is outside the recommended range."
        )

    if not 60 <= ft_len <= 100:
        warnings.append(
            f"Faculty teaser length ({ft_len} words) is outside the recommended range."
        )

    return ProjectTextGenerationResult(
        project_page=project_page,
        faculty_teaser=faculty_teaser,
        used_keywords=request.keywords,
        warnings=warnings or None,
    )

if __name__ == "__main__":
    mcp.run()
