from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

def evaluate_generated_vs_reference(
    *,
    project_id: str,
    generated_text: str,
    reference_text: str,
) -> dict:
    """
    Compare generated public-facing text against the real project description.
    """

    test_case = LLMTestCase(
        input="Compare generated project description to reference description.",
        actual_output=generated_text,
        expected_output=reference_text,
    )

    metric = AnswerRelevancyMetric()

    metric.measure(test_case)

    return {
        "project_id": project_id,
        "metric": "AnswerRelevancy",
        "score": metric.score,
        "reason": metric.reason,
    }
