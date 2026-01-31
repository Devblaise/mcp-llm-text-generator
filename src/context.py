from schemas import ProjectTextGenerationRequest

def build_context(request: ProjectTextGenerationRequest) -> str:
    audiences = ", ".join(a.value for a in request.target_audience)
    languages = ", ".join(request.languages)
    keywords = ", ".join(request.keywords) if request.keywords else "None provided"

    prompt = f"""
You are a science communication expert at a university working on public-facing research content.

PROJECT TITLE
{request.project_title}

KEYWORDS
{keywords}

TASK
Generate two texts based ONLY on the project title above:
- a detailed project page (300–500 words)
- a short faculty teaser (60–100 words)

TARGET AUDIENCE
{audiences}

LANGUAGES
Generate output in the following languages:
{languages}

READING LEVEL
For EACH generated text include:
- reading_level: one of [beginner, intermediate, advanced]

You must determine an appropriate reading level based on
target audience and content complexity.

STYLE GUIDELINES
- Popular science
- Clear explanations
- Avoid unnecessary jargon
- No internal proposal language

REQUIREMENTS
- Use clear, non-technical language appropriate for the audience
- Base all content strictly on the project title and keywords
- Avoid unverifiable claims or specific outcomes
- Integrate keywords naturally
- Keep descriptions high-level and generic where necessary

STRUCTURE (project page only)
Use clear section headers such as:
- Motivation
- Research Goals
- Societal Relevance
- Expected Impact
- Cooperation and Funding

OUTPUT FORMAT
Return strict JSON ONLY:

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

Replace <language_code> with each requested language (e.g., "en", "de").
"""

    return prompt.strip()
