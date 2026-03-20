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
      - Length: 300–400 words
      - Write as exactly 4 separate paragraphs — NO section headers or markdown headings.
      - Separate each paragraph with a blank line (\n\n).
      - Each paragraph covers one topic in order, without labelling it:
        1. Why the project exists (motivation/background)
        2. What the project does (research goals)
        3. Why it matters to society (societal relevance)
        4. What outcomes are expected (expected impact)

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
    - Preserve specific project details when available
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
