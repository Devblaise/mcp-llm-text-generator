def normalize_generated_entry(entry: dict) -> dict:
    """
    Ensures LLM output matches GeneratedText schema.
    Adds safe defaults if fields are missing.
    """

    # text should always exist, but guard anyway
    if "text" not in entry:
        entry["text"] = ""

    # Guardrail if LLM forgets reading_level
    if "reading_level" not in entry:
        entry["reading_level"] = "unknown"

    # Guardrail if LLM  forgets word_count
    if "word_count" not in entry:
        entry["word_count"] = len(entry["text"].split())

    return entry
