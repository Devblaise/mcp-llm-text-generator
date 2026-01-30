from schemas import ProjectTextGenerationRequest

def build_context(request: ProjectTextGenerationRequest) -> str:
    """
    Builds a single prompt for the LLM that requests both a detialed project page description
    and a short teaser for faculty teaser based only on sparse project metadata.
    """
    
    keywords_str = ", ".join(request.keywords)
    audiences = ", ".join(a.value for a in request.target_audience)
    reading_levels = ", ".join(r.value for r in request.reading_level)

    
    prompt = f"""
    You are an expert science communicator at the university.
    Your task is to generate two pieces of public-facing text based on minimal project metadata.
    
    INPUT DATA:
    - Project Title: {request.project_title}
    - Research Field: {request.research_field}
    - Keywords: {keywords_str}
    - Reading Level: {reading_levels}
    - Target Audience: {audiences}
    - Language: {request.language}
    
    TASK:
    1. Write a detailed but accessible project description suitable for a public project page.
    2. Write a short, engaging teaser suitable for a faculty overview page.

    LENGTH CONSTRAINTS:
    - Project page: approximately 300 to 500 words.
    - Faculty teaser: approximately 60 to 100 words.
    
    REQUIREMENTS:
    - Use clear, non-technical language appropriate for the target audience.
    - Base all content strictly on the title, research field, and keywords provided.
    - Aviod unverifiable claims or specific outcomes.
    - Integrate keywords naturally where appropriate.
    - Keep the description high-level and generic where necessary.
     
    GENERAL CONSTRAINTS
    -------------------
    - Write in {request.language}
    - Ensure consistency between both texts
    - Avoid unnecessary technical jargon
    
    OUTPUT FORMAT:
    Return a JSON object with the following structure:
    {{
        "project_page": {{
            "text": "...",
            "length_words": ...,
            "used_keywords": ["...", "..."]
        }},
        "faculty_teaser": {{
            "text": "...",
            "length_words": ...,
            "used_keywords": ["...", "..."]
        }},
        "warnings": ["..."] | null  # Optional notes about uncertainty or sparse input
    }}
    
    Only return valid JSON. DO not include explanations or additional text.
    """
    

    return prompt.strip()
