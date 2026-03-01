# keywords are extracted from these columns
_KEYWORD_COLS = ("Kooperationspartner", "Organisationseinheiten der Projektleitungen")

def extract_keywords(project: dict) -> list[str]:
    """Extract keywords from Kooperationspartner and Organisationseinheiten der Projektleitungen columns."""
    parts = [
        kw.strip()
        for col in _KEYWORD_COLS
        if (val := project.get(col)) and str(val).strip().lower() != "nan"
        for kw in str(val).replace(";", ",").split(",")
        if kw.strip()
    ]
    return list(dict.fromkeys(parts))  # deduplicate, preserve order


def normalize_generated_entry(entry: dict) -> dict:
    """
    Ensures LLM output matches GeneratedText schema.
    Adds safe defaults if fields are missing.
    """

    # text should always exist, but guard anyway
    if "text" not in entry:
        entry["text"] = ""

    # guard if LLM forgets reading_level
    if "reading_level" not in entry:
        entry["reading_level"] = "unknown"

    # guard if LLM forgets word_count
    if "word_count" not in entry:
        entry["word_count"] = len(entry["text"].split())

    return entry
