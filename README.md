# langchain-course

A small playground project for learning [LangChain](https://python.langchain.com/) by building a simple AI agent that can search the web.

## What it does

[main.py](main.py) wires up a LangChain agent with:

- **[Gemini](https://ai.google.dev/)** (`gemini-3.6-flash`) as the LLM, via `langchain-google-genai`
- **[Tavily Search](https://tavily.com/)** as a tool, via `langchain-tavily`

The agent is asked to find the current weather in Tokyo, and it uses the search tool to answer.

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) for dependency management
- API keys:
  - `GOOGLE_API_KEY` — for the Gemini model
  - `TAVILY_API_KEY` — for the Tavily search tool

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with your API keys:

   ```env
   GOOGLE_API_KEY=your-google-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ```

   `main.py` loads this file automatically via `python-dotenv`.

## Usage

Run the agent:

```bash
uv run main.py
```

This prints a greeting, then the agent's answer about the weather in Tokyo.

## Project structure

```
.
├── main.py          # Agent setup and entry point
├── pyproject.toml   # Project metadata and dependencies
└── uv.lock          # Locked dependency versions
```
