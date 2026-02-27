import streamlit as st
import json
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────
OUTPUTS_DIR = Path(__file__).parent / "src" / "outputs"
REFERENCES_DIR = Path(__file__).parent / "src" / "data" / "references"

st.set_page_config(
    page_title="BA Creation of internet entries with MCP Server – Results",
    layout="wide",
)

# ─── Custom styling ──────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1a1a2e;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .section-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Helper functions ────────────────────────────────────────

@st.cache_data
def load_projects() -> list[str]:
    """Return sorted list of project IDs that have output.json."""
    if not OUTPUTS_DIR.exists():
        return []
    return sorted(
        p.name for p in OUTPUTS_DIR.iterdir()
        if p.is_dir() and (p / "output.json").exists()
    )


@st.cache_data
def load_output(project_id: str) -> dict | None:
    path = OUTPUTS_DIR / project_id / "output.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


@st.cache_data
def load_evaluation(project_id: str) -> dict | None:
    path = OUTPUTS_DIR / project_id / "evaluation.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


@st.cache_data
def load_reference(project_id: str) -> str | None:
    path = REFERENCES_DIR / f"{project_id}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return None


def lang_label(code: str) -> str:
    return {"de": "German", "en": "English"}.get(code, code.upper())


# ─── Sidebar ─────────────────────────────────────────────────

st.sidebar.markdown("### Project Selection")

projects = load_projects()
if not projects:
    st.error("No generated outputs found. Run the text generator first.")
    st.stop()

selected = st.sidebar.selectbox("Project", projects, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(projects)}** projects generated")

evaluation = load_evaluation(selected)
if evaluation and "semantic_similarity" in evaluation:
    score = evaluation["semantic_similarity"]
    st.sidebar.metric("Similarity", f"{score:.2%}")

# Download buttons in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Download")

_output = load_output(selected)
if _output:
    st.sidebar.download_button(
        "Output JSON",
        data=json.dumps(_output, indent=2, ensure_ascii=False),
        file_name=f"{selected}_output.json",
        mime="application/json",
    )

_eval = load_evaluation(selected)
if _eval:
    st.sidebar.download_button(
        "Evaluation JSON",
        data=json.dumps(_eval, indent=2, ensure_ascii=False),
        file_name=f"{selected}_evaluation.json",
        mime="application/json",
    )

_ref = load_reference(selected)
if _ref:
    st.sidebar.download_button(
        "Reference Text",
        data=_ref,
        file_name=f"{selected}_reference.txt",
        mime="text/plain",
    )


# ─── Main Content ────────────────────────────────────────────

st.markdown(f'<div class="main-header">{selected}</div>', unsafe_allow_html=True)

output = load_output(selected)
if not output:
    st.error("Could not load output data for this project.")
    st.stop()

tab_page, tab_teaser, tab_eval, tab_ref = st.tabs([
    "Project Page", "Faculty Teaser", "Evaluation", "Reference Text"
])


# ── Tab 1: Project Page ─────────────────────────────────────
with tab_page:
    page_data = output.get("project_page", {})
    langs = list(page_data.keys())

    if not langs:
        st.warning("No project page texts available.")
    elif len(langs) == 1:
        lang = langs[0]
        entry = page_data[lang]
        st.markdown(f'<p class="section-label">{lang_label(lang)}</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Word Count", entry.get("word_count", "–"))
        c2.metric("Reading Level", (entry.get("reading_level") or "–").capitalize())
        st.markdown("---")
        st.markdown(entry.get("text", ""))
    else:
        cols = st.columns(len(langs))
        for col, lang in zip(cols, langs):
            entry = page_data[lang]
            with col:
                st.markdown(f'<p class="section-label">{lang_label(lang)}</p>', unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.metric("Words", entry.get("word_count", "–"))
                m2.metric("Level", (entry.get("reading_level") or "–").capitalize())
                st.markdown("---")
                st.markdown(entry.get("text", ""))


# ── Tab 2: Faculty Teaser ───────────────────────────────────
with tab_teaser:
    teaser_data = output.get("faculty_teaser", {})
    langs = list(teaser_data.keys())

    if not langs:
        st.warning("No faculty teaser texts available.")
    elif len(langs) == 1:
        lang = langs[0]
        entry = teaser_data[lang]
        st.markdown(f'<p class="section-label">{lang_label(lang)}</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Word Count", entry.get("word_count", "–"))
        c2.metric("Reading Level", (entry.get("reading_level") or "–").capitalize())
        st.markdown("---")
        st.markdown(entry.get("text", ""))
    else:
        cols = st.columns(len(langs))
        for col, lang in zip(cols, langs):
            entry = teaser_data[lang]
            with col:
                st.markdown(f'<p class="section-label">{lang_label(lang)}</p>', unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.metric("Words", entry.get("word_count", "–"))
                m2.metric("Level", (entry.get("reading_level") or "–").capitalize())
                st.markdown("---")
                st.markdown(entry.get("text", ""))


# ── Tab 3: Evaluation ──────────────────────────────────────
with tab_eval:
    if not evaluation:
        st.info(
            "No evaluation data for this project. "
            "Place a reference text in src/data/references/ and regenerate."
        )
    elif "metrics" in evaluation and evaluation["metrics"] is None:
        st.warning(evaluation.get("reason", "Evaluation was skipped."))
    else:
        score = evaluation.get("semantic_similarity", 0)

        st.markdown('<p class="section-label">Semantic Similarity</p>', unsafe_allow_html=True)

        col_score, col_detail = st.columns([1, 2])

        with col_score:
            st.metric("Cosine Similarity", f"{score:.4f}")
            st.progress(min(score, 1.0))

            if score >= 0.85:
                label, color = "Very High", "#2e7d32"
            elif score >= 0.70:
                label, color = "High", "#1565c0"
            elif score >= 0.50:
                label, color = "Moderate", "#ef6c00"
            else:
                label, color = "Low", "#c62828"

            st.markdown(
                f'<span style="color:{color}; font-weight:600;">{label} similarity</span>',
                unsafe_allow_html=True,
            )

        with col_detail:
            st.caption(
                "Cosine similarity measures semantic closeness between the generated "
                "and reference text embeddings. A score of 1.0 indicates identical meaning, "
                "0.0 indicates no semantic overlap."
            )

        emb = evaluation.get("embedding_details", {})
        if emb:
            st.markdown("---")
            st.markdown('<p class="section-label">Model Details</p>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.markdown(f"**Model:** `{emb.get('model', '–')}`")
            c2.markdown(f"**Embedding Dimensions:** `{emb.get('dimensions', '–')}`")

            with st.expander("Embedding samples (first 10 dimensions)"):
                sample_cols = st.columns(2)
                with sample_cols[0]:
                    st.caption("Generated")
                    st.code(str(emb.get("generated_embedding_sample", [])))
                with sample_cols[1]:
                    st.caption("Reference")
                    st.code(str(emb.get("reference_embedding_sample", [])))

        excerpt = evaluation.get("reference_excerpt", "")
        if excerpt:
            st.markdown("---")
            st.markdown('<p class="section-label">Reference Excerpt</p>', unsafe_allow_html=True)
            st.text(excerpt)


# ── Tab 4: Reference Text ──────────────────────────────────
with tab_ref:
    ref_text = load_reference(selected)
    if ref_text:
        st.markdown('<p class="section-label">Human-Written Reference</p>', unsafe_allow_html=True)
        st.markdown(ref_text)
        word_count = len(ref_text.split())
        st.caption(f"{word_count} words")
    else:
        st.info(
            f"No reference file found for {selected}. "
            "Add a .txt file to src/data/references/ to enable evaluation."
        )
