# Project-07-Multi-Agent-Web-Research-and-Synthesis-Engine

An autonomous AI system that uses a team of interacting agents to search, read, analyse, and write up web research as a polished report — with a Streamlit interface for watching the whole process happen live. Built with Python, LangChain, and the OpenAI and Tavily APIs.

## Overview

**MARA** (Multi-Agent Research & Analysis) is a fully autonomous, production-style agentic AI system. Instead of a single model answering a question in one pass, it runs a **pipeline of five specialised agents** that each do one part of the job — search, plan, analyse, write, and review — and hand their work to the next agent in line. The result is a sourced, structured research report rather than a one-shot chat reply.

The included Streamlit app (`app.py`) visualises this pipeline as a "case file": a live timeline tracks the query from intake through to a compiled report, and every agent's intermediate output is available to inspect.

## Architecture: The Agent Team

The pipeline (`pipeline.py`) orchestrates five agents, defined in `agents.py` and backed by the tools in `tools.py`:

| Agent | Role |
|---|---|
| **Research Agent** | Searches the web (via the Tavily API) and gathers raw sources and findings on the topic. |
| **Planning Agent** | Structures the investigation — turning raw findings into an outline for the report. |
| **Analysis Agent** | Weighs the evidence gathered and concludes it. |
| **Writer Agent** | Synthesises everything into a comprehensive, professional report draft. |
| **Reviewer Agent** | Critiques the draft for gaps, bias, or weak sourcing, and produces the final feedback notes. |

All five agents share context through the pipeline's run, so later agents build directly on earlier agents' output rather than starting from scratch.

## Tech Stack

- **Language:** Python 3.10+
- **Agent framework:** LangChain (LCEL)
- **LLM:** OpenAI API
- **Web search/retrieval:** Tavily API
- **Interface:** Streamlit (`app.py`)
- **Dependency management:** [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`), with `requirements.txt` provided as a pip-compatible fallback

## Project Structure

```
.
├── agents.py                              # Agent definitions (Research, Planning, Analysis, Writer, Reviewer)
├── app.py                                 # Streamlit UI — run this to use the app interactively
├── main.py                                # CLI entry point for running the pipeline without the UI
├── pipeline.py                            # Orchestrates the agent pipeline end-to-end
├── tools.py                               # Tool definitions the agents call (e.g. Tavily web search)
├── pyproject.toml / uv.lock                # Project + locked dependencies (uv)
├── requirements.txt                        # Dependencies (pip fallback)
├── Multi-Agent Autonomous System.pdf       # Written design/architecture overview of the system
├── LICENSE
└── README.md
```

## Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/Project-07-Multi-Agent-Web-Research-and-Synthesis-Engine.git
cd Project-07-Multi-Agent-Web-Research-and-Synthesis-Engine
```

### 2. Install dependencies

Using **uv** (recommended — matches the committed `uv.lock`):

```bash
uv sync
```

Or with **pip**:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up your API keys

This project needs your own API keys for OpenAI and Tavily — **no keys are included in this repo, and it will not run without them.**

1. Get an OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys).
2. Get a Tavily API key (free tier available) from [tavily.com](https://tavily.com/).
3. In the project root, create a file named **`.env`** (this file is git-ignored and should never be committed) with the following contents:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

That's it — the app loads these automatically at startup. If either key is missing or invalid, the pipeline will fail when it tries to call that service, so double-check both are set before running.

> ⚠️ Both APIs are paid/metered beyond their free tiers. Running research queries will consume your own API credits.

## Usage

### Option A — Streamlit app (recommended)

```bash
streamlit run app.py
```

This opens the interface in your browser. Enter a research question, click **"Open the Case,"** and watch the case timeline move through Research → Planning → Analysis → Writing → Review while the agents work. When it finishes, you get:

- A live pipeline log with each agent's raw output
- A compiled final report (downloadable as Markdown)
- Reviewer notes critiquing the report
- A list of sources used

### Option B — Command line

```bash
python main.py
```

Runs the same pipeline directly in the terminal — useful for scripting or for environments without a browser.

## Documentation

See `Multi-Agent Autonomous System.pdf` in this repo for a fuller write-up of the system's design and architecture.

## License

See [LICENSE](./LICENSE) for details.
