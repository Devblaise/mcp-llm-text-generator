# BA Creation of internet entries with MCP Server

An MCP (Model Context Protocol) server that generates public-facing university project page content using a large language model. It reads project metadata from an Excel file, builds a structured prompt, and produces bilingual (German/English) texts with automatic quality evaluation.

## Overview

This project provides two MCP tools:

- **generate_project_text** — Takes project metadata and generates a structured project page description and faculty teaser in multiple languages.
- **generate_project_text_from_project_id** — Looks up a project by its abbreviation (Abkürzung) from the Excel data and calls the first tool automatically.

- **FastAPI dashboard** for viewing results, evaluation scores, and downloading outputs.

## Project Structure

```
├── app.py                 # Data outputs UI app
├── main.py                # Alternative entrypoint
├── pyproject.toml         # Project dependencies
├── templates/
│   ├── index.html         # UI landing page
│   └── project.html       # Project detail view
├── src/
│   ├── server.py          # MCP server entrypoint
│   ├── mcp_app.py         # MCP instance
│   ├── tools.py           # MCP tool definitions
│   ├── resources.py       # MCP resource (Excel reader)
│   ├── context.py         # Prompt builder
│   ├── llm.py             # LLM client (OpenAI-compatible API)
│   ├── evaluation.py      # LangCheck metric evaluation
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
- Access to a GWDG API key (OpenAI-compatible endpoint) or alternative API key (OpenAI, Gemini, etc.)
- GWDG key usage documentation: https://docs.hpc.gwdg.de/services/saia/index.html


## Installation

### 1. Get the source code

1. Go to the repository: https://github.com/Devblaise/Creation-of-internet-entries-with-MCP-Server
2. Fork the repo or click **Code → Download ZIP**
3. Extract the ZIP to a folder if downloaded

### 2. Install UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install dependencies

```bash
cd "BA Creation of internet entries with MCP Server"
uv venv
```

Activate the virtual environment:

```bash
# macOS/Linux
source .venv/bin/activate
```

```powershell
# Windows (PowerShell)
.venv\Scripts\activate
```

Then install all dependencies:

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
GWDG_API_KEY=your_api_key_here
GWDG_API_BASE=your_api_base_url_here
```
Add excel data file in filepath: ``` src/data/<excel_data> ```

## Usage

### Run the MCP server (with Inspector UI)

```bash
mcp dev src/server.py
```

This opens the MCP Inspector at `http://localhost:6274` where you can test the tools interactively.


### View results in the dashboard

```bash
uvicorn app:app 
```
Opens at `http://localhost:8000`. where you view generated outputs


#### Generate text for a project

In the MCP Inspector, call the `generate_project_text_from_project_id` tool with:

```json
{
  "project_id": "REACH"
}
```

The project ID corresponds to the **Abkürzung** column in the Excel file. The lookup is case-insensitive.

### View results in the dashboard

- Side-by-side German/English generated texts
- Semantic similarity, Factual Consistency, Rogue-L
- Reference text comparison
- Downloadable JSON outputs and reference files

## Evaluation

Generated texts are evaluated against human-written references using LangCheck semantic similarity , factual consistency and Rogue-L

- **Runs locally** — no external API needed for evaluation

Place reference texts as `.txt` files in `src/data/references/` named by the project abbreviation (e.g., `REACH.txt`).

## Technologies

- **FastMCP** — MCP server framework
- **OpenAI API** (GWDG endpoint) — Text generation
- **Langcheck** — Semantic similarity, factual consistency and Rogue-L
- **FastAPI + Jinja2** — Results output data dashboard
- **Pandas** — Excel data processing
- **Pydantic** — Input/output validation

