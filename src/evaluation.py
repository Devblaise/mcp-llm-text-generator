#**************************************
# Author: Mbadugha Kenechukwu
# Technichse Hoschule Köln (TH Köln)
# Communication Systems and Networks
#*************************************

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from llm import generate_text_from_context 

#-------------------------
# EVALUATION LOGIC
#-------------------------  

def judge_llm(prompt: str) -> str:
    """
    Uses the project LLM to perform qualitative comparison.
    Returns a short comparison paragraph.
    """
    return generate_text_from_context(prompt)


def evaluate_generated_vs_reference(
    *,
    project_id: str,
    generated_text: str,
    reference_text: str,
    ) -> dict:
    """
    Offline benchmark:
    Compare generated public-facing text against the real human-written project description.
    """
    
    # --- Guard rail if Excel has no human written project description ---
    if not reference_text or not reference_text.strip():
        return {
            "project_id": project_id,
            "metric": "AnswerRelevancy",
            "score": None,
            "reason": "Reference description missing — evaluation skipped.",
            "llm_comparison": None,
            "reference_excerpt": None,
        }
      
    # --- Quantitative evaluation (DeepEval)---  
    test_case = LLMTestCase(
        input= reference_text,
        actual_output= generated_text,
    )

    
    metric = AnswerRelevancyMetric(threshold=0.7)
    metric.measure(test_case)
    
    # ---  Qualitative explanation (non-scoring) ---
    comparison_prompt = f"""
    Compare the following two project descriptions.

    Generated description:
    {generated_text}

    Reference description:
    {reference_text}

    Explain briefly how closely the generated description matches the reference.
    """

    
    llm_comparison = judge_llm(comparison_prompt)

    return {
        "project_id": project_id,
        "metric": "AnswerRelevancy",
        "score": metric.score,
        "reason": metric.reason,
        "llm_comparison": llm_comparison,
        "reference_excerpt": reference_text[:300],  # store part of the human written description for traceability and transparency
    }
