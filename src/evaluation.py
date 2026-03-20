import logging
import sys
import contextlib
import langcheck.metrics as metrics

# -------------------------
# LLM TEXT EVALUATION
# Uses LangCheck metrics 
# -------------------------

def evaluate_generated_vs_reference(
    *,
    project_id: str,
    generated_text: str,
    human_reference_text: str,
) -> dict:
    """
    Compare generated text against human-written reference
    using multiple evaluation metrics.

    Metrics:
    - semantic similarity (langcheck)
    - factual consistency (vs. human reference)
    - ROUGE-L
    """

    if not human_reference_text or not human_reference_text.strip():
        return {
            "project_id": project_id,
            "metrics": None,
            "reason": "Reference description missing — evaluation skipped.",
        }

    try:

        # Redirect stdout to stderr to prevent library warnings from
        # corrupting the MCP JSON-RPC stream on stdout
        with contextlib.redirect_stdout(sys.stderr):
            # Semantic similarity (langcheck)
            semantic_similarity = metrics.semantic_similarity(
                generated_text,
                human_reference_text
            ).metric_values[0]

            # Factual consistency (vs. human reference)
            factual_consistency = metrics.factual_consistency(
                generated_text,
                human_reference_text
            ).metric_values[0]

            # ROUGE-L
            rouge_l = metrics.rougeL(
                generated_text,
                human_reference_text
            ).metric_values[0]

        return {
            "project_id": project_id,
            "metrics": {
                "semantic_similarity": round(semantic_similarity, 4),
                "factual_consistency": round(factual_consistency, 4),
                "rouge_l": round(rouge_l, 4),
            },
            "reference_excerpt": human_reference_text[:300],
        }

    except Exception as e:
        logging.error(f"Evaluation failed for {project_id}: {e}")
        return {
            "project_id": project_id,
            "metrics": None,
            "reason": f"Evaluation error: {e}",
        }