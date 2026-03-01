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
    You are a science communicator expert writing for an educated general audience 
    with no specialist background. 

    Your task is to rewrite the provided project description  into
    clear, structured texts suitable for a university website.

    ────────────────────────────────────────
    SOURCE TEXT (EXCEL: Beschreibung)
    ────────────────────────────────────────

    Project description:
    {request.project_description}

    Keywords (must appear in the generated text):
    {keywords}

    IMPORTANT RULES:
    - The project description is the PRIMARY source of truth.
    - Preserve concrete entities, tools, technologies, and scenarios when present.
    - Integrate ALL provided keywords naturally into the generated text.
    - Do NOT introduce new concepts beyond what keywords and description provide.
    - Prefer factual consistency over creativity.

    ────────────────────────────────────────
    TASK
    ────────────────────────────────────────

    Generate TWO texts:

    1. Project Page Description
      - Length: 400–500 words
      - Structure with EXACTLY these section headers (using ### markdown):

        For German (de):
          ### Motivation
          ### Forschungsziele
          ### Gesellschaftliche Relevanz
          ### Erwarteter Einfluss

        For English (en):
          ### Motivation
          ### Research Goals
          ### Societal Relevance
          ### Expected Impact

      - Use the EXACT headers above. Do NOT rename, reorder, or skip any section.

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

    Select based on audience and technical density.

    ────────────────────────────────────────
    STYLE GUIDELINES
    ────────────────────────────────────────

    - Write for a PUBLIC-FACING university website, NOT an academic paper
    - Use clear, simple language that non-experts can understand
    - Avoid jargon — if technical terms are necessary, briefly explain them
    - Short sentences and paragraphs for easy readability
    - Active voice preferred over passive voice
    - Engaging and informative tone, like a well-written magazine article
    - Preserve specific project details when available
    - No academic phrasing (avoid "furthermore", "moreover", "it should be noted")
    - No proposal language ("we aim to", "this project seeks to")
    - No unverifiable claims
    - Target reading level: general public with interest in science/technology

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
