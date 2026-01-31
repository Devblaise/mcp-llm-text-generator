from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# -------------------------
# ENUMS
# -------------------------
class LanguageCode(str, Enum):
    en = "en"
    de = "de"

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
    keywords: List[str] = Field(..., description="Key terms describing the project.")
    target_audience: list[TargetAudience] = Field(..., description="Intended readership groups.")
    languages: List[LanguageCode] = Field(..., description="Output language (e.g., ['en', 'de']).")
    source_type: str | None = Field(None, description="Origin of the input data.") 

# -------------------------
# OUTPUT SCHEMA
# -------------------------

class GeneratedText(BaseModel):
    text: str = Field(..., description="Generated public-facing text.") 
    reading_level: Optional[str]= Field(..., description="Intended reading level of the text.")
    word_count: int = 0
   

class ProjectTextGenerationResult(BaseModel):
    project_page: dict[str, GeneratedText] = Field(..., description="Detailed project description for a public project page.")
    faculty_teaser: dict[str, GeneratedText] = Field(..., description="Short teaser text for a faculty overview page.") 
    used_keywords: Optional[List[str]]= Field(..., description="Keywords that appear in the text.") 
    warnings: Optional[List[str]] = Field(None, description="Notes about uncertainty or sparse input.") 
