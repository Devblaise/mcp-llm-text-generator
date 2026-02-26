from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from llm import generate_text_from_context
import logging

async def judge_llm(prompt: str) -> str:
    """Uses the project LLM to perform qualitative comparison."""
    return await generate_text_from_context(prompt)


async def evaluate_generated_vs_reference(
    *,
    project_id: str,
    generated_text: str,
    human_reference_text: str,
) -> dict:
    """Compare generated text against human-written reference."""
    
    if not human_reference_text or not human_reference_text.strip():
        return {
            "project_id": project_id,
            "metric": "TextSimilarity",
            "score": None,
            "reason": "Reference description missing — evaluation skipped.",
            "llm_comparison": None,
            "reference_excerpt": None,
        }
    
    # --- Quantitative evaluation ---
    test_case = LLMTestCase(
        input="Compare these project descriptions",
        actual_output=generated_text,
        expected_output=human_reference_text,
    )
    
    metric = GEval(
        name="TextSimilarity",
        criteria="Evaluate if the generated text preserves key facts, tone, and structure from the reference",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        threshold=0.7,
    )
    
    try:
        await metric.a_measure(test_case)
        score = metric.score
        reason = metric.reason
    except Exception as e:
        logging.error(f"DeepEval evaluation failed: {e}")
        score = None
        reason = f"Evaluation error: {e}"
    
    # --- Qualitative explanation ---
    comparison_prompt = f"""
    Compare the following two project descriptions.

    Generated description:
    {generated_text}

    Reference description:
    {human_reference_text}

    Explain briefly how closely the generated description matches the reference.
    """
    
    llm_comparison = await judge_llm(comparison_prompt)
    
    return {
        "project_id": project_id,
        "metric": "TextSimilarity",
        "score": score,
        "reason": reason,
        "llm_comparison": llm_comparison,
        "reference_excerpt": human_reference_text[:300],
    }
