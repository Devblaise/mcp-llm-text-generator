from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# -------------------------
# ENUMS
# -------------------------

class TargetAudience(str, Enum):
    faculty = "faculty"
    students = "students"
    industry = "industry"
    general_public = "general_public"

class ReadingLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class SourceType(str, Enum):
    database = "database"
    excel = "excel"

# -------------------------
# INPUT SCHEMA
# -------------------------

class ProjectTextGenerationRequest(BaseModel):
    project_title: str = Field(..., description="Short title of the research project.")
    research_field: str = Field(..., description="High-level research domain.") 
    keywords: List[str] = Field(..., description="Key terms describing the project.")
    target_audience: list[TargetAudience] = Field(..., description="Intended readership groups.")
    reading_level: list[ReadingLevel] = Field(..., description="Estimated reading complexity.")
    language: str = Field(..., description="Output language (e.g., 'en', 'de').")
    source_type: Optional[SourceType] = Field(None, description="Origin of the input data.") 

# -------------------------
# OUTPUT SCHEMA
# -------------------------

class GeneratedText(BaseModel):
    text: str = Field(..., description="Generated public-facing text.") 
    length_words: int = Field(...,  description="Word count of the generated text.") 
    used_keywords: List[str] = Field(..., description="Keywords that appear in the text.") 

class ProjectTextGenerationResult(BaseModel):
    project_page: GeneratedText = Field(..., description="Detailed project description for a public project page.")
    faculty_teaser: GeneratedText = Field(..., description="Short teaser text for a faculty overview page.") 
    warnings: Optional[List[str]] = Field(None, description="Notes about uncertainty or sparse input.") 
