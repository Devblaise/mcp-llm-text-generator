# BA Creation of internet entries with MCP Server

An MCP (Model Context Protocol) server that generates public-facing university project page content using a large language model. It reads project metadata from an Excel file, builds a structured prompt, and produces bilingual (German/English) texts with automatic quality evaluation.

## Overview

This project provides two MCP tools:

- **generate_project_text** — Takes project metadata and generates a structured project page description and faculty teaser in multiple languages.
- **generate_project_text_from_project_id** — Looks up a project by its abbreviation (Abkürzung) from the Excel data and calls the first tool automatically.

It also includes:

- **Semantic evaluation** using sentence-transformers to compare generated text against human-written references.
- **Streamlit dashboard** for viewing results, evaluation scores, and downloading outputs.

## Project Structure

```
├── dashboard.py           # Streamlit dashboard for viewing results
├── main.py                # Alternative entrypoint
├── pyproject.toml         # Project dependencies
├── src/
│   ├── server.py          # MCP server entrypoint
│   ├── mcp_app.py         # FastMCP instance
│   ├── tools.py           # MCP tool definitions
│   ├── resources.py       # MCP resource (Excel reader)
│   ├── context.py         # Prompt builder
│   ├── llm.py             # LLM client (OpenAI-compatible API)
│   ├── evaluation.py      # Semantic similarity evaluation
│   ├── storage.py         # File I/O (save outputs, load references)
│   ├── schemas.py         # Pydantic input/output models
│   ├── utils.py           # Keyword extraction, output normalization
│   ├── data/
│   │   ├── references/    # Human-written reference texts (.txt)
│   │   └── *.xlsx         # Project metadata Excel file
│   └── outputs/           # Generated outputs and evaluation results
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Access to a GWDG API key (OpenAI-compatible endpoint)

## Installation

### 1. Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Set up the project

```bash
cd mcp-llm-text-generator
uv venv
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
GWDG_API_KEY=your_api_key_here
GWDG_API_BASE=your_api_base_url_here
```

## Usage

### Run the MCP server (with Inspector UI)

```bash
uv run mcp dev src/server.py
```

This opens the MCP Inspector at `http://localhost:6274` where you can test the tools interactively.

### Generate text for a project

In the MCP Inspector, call the `generate_project_text_from_project_id` tool with:

```json
{
  "project_id": "REACH"
}
```

The project ID corresponds to the **Abkürzung** column in the Excel file. The lookup is case-insensitive.

### View results in the dashboard

```bash
uv run streamlit run dashboard.py
```

Opens at `http://localhost:8501` with:

- Side-by-side German/English generated texts
- Word counts and reading levels
- Semantic similarity evaluation scores
- Downloadable JSON outputs

## Evaluation

Generated texts are evaluated against human-written references using cosine similarity of sentence embeddings:

- **Model:** paraphrase-multilingual-MiniLM-L12-v2
- **Method:** Cosine similarity between generated and reference text embeddings
- **Runs locally** — no external API needed for evaluation

Place reference texts as `.txt` files in `src/data/references/` named by the project abbreviation (e.g., `REACH.txt`).

## Technologies

- **FastMCP** — MCP server framework
- **OpenAI API** (GWDG endpoint) — Text generation
- **sentence-transformers** — Semantic similarity evaluation
- **Streamlit** — Results dashboard
- **Pandas** — Excel data processing
- **Pydantic** — Input/output validation