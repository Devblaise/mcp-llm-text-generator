from schemas import GenerateProjectTextInput

#-------------------------
# CONTEXT BUILDING
#-------------------------  

def build_context(request: GenerateProjectTextInput) -> str:
    """
    Builds a controlled prompt for public-facing text generation
    based exclusively on high-level project metadata.
    The prompt is designed to guide the LLM in generating structured,
    coherent, and audience-appropriate content.
    """

    audiences = ", ".join(a.value for a in request.target_audience)
    languages = ", ".join(lang.value for lang in request.languages)
    keywords = ", ".join(request.keywords) if request.keywords else "None"

    prompt = f"""
    You are writing official university project page content.

    Your task is to rewrite the provided project description into
    clear, structured texts suitable for a university website.


    ────────────────────────────────────────
    SOURCE TEXT (EXCEL: Beschreibung)
    ────────────────────────────────────────

    Project description:
    {request.project_description}

    Optional Keywords  (contextual hints only):
    {keywords}

    IMPORTANT RULES:
    - The project description is the PRIMARY source of truth.
    - Preserve concrete entities, tools, technologies, and scenarios when present.
    - Keywords are optional reinforcement only.
    - Do NOT introduce new concepts based only on keywords.
    - Prefer factual consistency over creativity.

    ────────────────────────────────────────
    TASK
    ────────────────────────────────────────

    Generate TWO texts:

    1. Project Page Description
      - Length: 400–500 words
      - Structure with clear section headers:
        • Motivation
        • Research Goals
        • Societal Relevance
        • Expected Impact
        • Cooperation and Funding 

    2. Faculty Teaser
      - Length: 50–100 words
      - Concise institutional summary.

    ────────────────────────────────────────
    TARGET AUDIENCE
    ────────────────────────────────────────

    {audiences}

    ────────────────────────────────────────
    LANGUAGES
    ────────────────────────────────────────

    Generate output in the following languages:
    {languages}

    ────────────────────────────────────────
    READING LEVEL
    ────────────────────────────────────────

    For EACH text choose:
    - beginner
    - intermediate
    - advanced

    Select based on audience and technical density.

    ────────────────────────────────────────
    STYLE GUIDELINES
    ────────────────────────────────────────

    - Institutional university project style
    - Clear and concrete wording
    - Preserve specific project details when available
    - Neutral, factual tone
    - No proposal language
    - No unverifiable claims

    ────────────────────────────────────────
    OUTPUT FORMAT (STRICT JSON)
    ────────────────────────────────────────

    {{
      "project_page": {{
        "<language_code>": {{
          "text": "...",
          "reading_level": "...",
          "word_count": ...
        }}
      }},
      "faculty_teaser": {{
        "<language_code>": {{
          "text": "...",
          "reading_level": "...",
          "word_count": ...
        }}
      }},
      "used_keywords": ["..."],
      "warnings": ["..."]
    }}

    Replace <language_code> with each requested language.

    Return ONLY valid JSON.
    """

    return prompt.strip()
