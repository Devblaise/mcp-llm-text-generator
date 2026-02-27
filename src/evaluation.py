import logging
from sentence_transformers import SentenceTransformer, util

#-------------------------
# SEMANTIC SIMILARITY EVALUATION
# Uses sentence-transformers (local, no API needed)
# Reference: https://www.sbert.net/
#-------------------------

# Load model once (multilingual - supports German)
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return _model


def evaluate_generated_vs_reference(
    *,
    project_id: str,
    generated_text: str,
    human_reference_text: str,
) -> dict:
    """
    Compare generated text against human-written reference using semantic similarity.
    
    Uses sentence-transformers to compute cosine similarity between embeddings.
    This measures how semantically similar the texts are, not just word overlap.
    
    Reference: https://www.sbert.net/docs/usage/semantic_textual_similarity.html
    """
    
    if not human_reference_text or not human_reference_text.strip():
        return {
            "project_id": project_id,
            "metrics": None,
            "reason": "Reference description missing — evaluation skipped.",
        }
    
    try:
        model = _get_model()
        
        # Compute embeddings
        emb_generated = model.encode(generated_text, convert_to_tensor=True)
        emb_reference = model.encode(human_reference_text, convert_to_tensor=True)
        
        # Compute cosine similarity
        similarity = util.cos_sim(emb_generated, emb_reference).item()
        
        # Get embedding statistics for output
        emb_gen_list = emb_generated.tolist()
        emb_ref_list = emb_reference.tolist()
        
        return {
            "project_id": project_id,
            "semantic_similarity": round(similarity, 4),
            "embedding_details": {
                "model": "paraphrase-multilingual-MiniLM-L12-v2",
                "dimensions": len(emb_gen_list),
                "generated_embedding_sample": [round(x, 4) for x in emb_gen_list[:10]],  # First 10 values
                "reference_embedding_sample": [round(x, 4) for x in emb_ref_list[:10]],  # First 10 values
            },
            "reference_excerpt": human_reference_text[:300],
        }
        
    except Exception as e:
        logging.error(f"Evaluation failed: {e}")
        return {
            "project_id": project_id,
            "metrics": None,
            "reason": f"Evaluation error: {e}",
        }
