from context import build_context
from schemas import ProjectTextGenerationRequest


def main():
    request = ProjectTextGenerationRequest(
        project_title="AI in Healthcare",
        research_field="Artificial Intelligence",
        keywords=["machine learning", "diagnostics","diagnostics", "healthcare"],
        target_audience=["general_public", "students"],
        language="en"
    )

    prompt = build_context(request)
    print("=== GENERATED PROMPT ===\n")
    print(prompt)


if __name__ == "__main__":
    main()
