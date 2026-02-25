from schemas import GenerateProjectTextInput

#-------------------------
# CONTEXT BUILDING
#-------------------------  

def build_context(request: GenerateProjectTextInput) -> str:
    """
    Builds a controlled prompt for public-facing text generation
    based exclusively on high-level project metadata.

    IMPORTANT:
    - The original technical project description is NOT used.
    - All content must be inferred from title and metadata only.
    """

    audiences = ", ".join(a.value for a in request.target_audience)
    languages = ", ".join(lang.value for lang in request.languages)
    keywords = ", ".join(request.keywords) if request.keywords else "None"

    prompt = f"""
    You are a science communication expert at a university.

    Your task is to generate public-facing descriptions of a research project
    using ONLY high-level metadata provided below.

    ────────────────────────────────────────
    PROJECT METADATA (SOURCE: EXCEL SHEET)
    ────────────────────────────────────────

    Project description:
    {request.project_description}

    Keywords and contextual signals:
    {keywords}

    IMPORTANT CONSTRAINT:
    - The original technical project description exists but MUST NOT be used.
    - Do NOT infer specific results, methods, or claims.
    - Keep all descriptions high-level and generic where necessary.

    ────────────────────────────────────────
    TASK
    ────────────────────────────────────────

    Generate TWO texts:

    1. Project Page Description
      - Length: 200–250 words
      - Structure with clear section headers:
        • Motivation
        • Research Goals
        • Societal Relevance
        • Expected Impact
        • Cooperation and Funding (general)

    2. Faculty Teaser
      - Length: 50–100 words
      - Concise, accessible summary

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

    For EACH generated text, determine an appropriate reading level:
    - beginner
    - intermediate
    - advanced

    Choose based on audience and content complexity.

    ────────────────────────────────────────
    STYLE GUIDELINES
    ────────────────────────────────────────

    - Popular science tone
    - Clear explanations
    - No proposal language
    - No internal references
    - No unverifiable claims
    - Neutral, informative style

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

    Replace <language_code> with each requested language (e.g. "de", "en").

    Return ONLY valid JSON.
    """

    return prompt.strip()
