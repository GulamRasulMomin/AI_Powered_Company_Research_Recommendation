# AI-Powered Company Research Recommendation

A Streamlit application that turns a company name into a structured research and sales-intelligence brief. It combines web search through Tavily with a Groq-hosted language model and a LangGraph workflow.

## Features

- Company overview
- Current business information
- Potential business challenges
- Practical AI opportunities
- Personalized, CEO-ready pitch
- Interactive report sections in a Streamlit interface

## Requirements

- Python 3.10 or newer
- A Groq API key
- A Tavily API key

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   python -m pip install -r requirement.txt
   ```

   With `uv`, use:

   ```powershell
   uv pip install -r requirement.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Do not commit `.env`; it is excluded by [.gitignore](.gitignore).

## Run the app

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, enter a company name, and select **Generate intelligence report**.

## How It Works

The LangGraph workflow starts the company overview and business information research in parallel. It then uses those results to generate:

1. Potential business challenges
2. AI opportunities
3. A personalized pitch

The language model is configured in `llm.py` as `openai/gpt-oss-120b` through Groq. Web search is configured in `web_search.py` through Tavily.

## Project Structure

```text
.
├── app.py                         # Streamlit user interface
├── graph.py                       # LangGraph workflow
├── llm.py                         # Groq LLM configuration
├── state.py                       # Shared research state
├── web_search.py                  # Tavily search helper
├── requirement.txt                # Python dependencies
└── agents/                        # Research workflow nodes
    ├── ai_opportunities.py
    ├── business_challenges.py
    ├── business_information.py
    ├── company_overview.py
    └── personalized_pitch.py
```

## Notes

The generated report is based on publicly available search results and model-generated analysis. Review the sources and recommendations before using the output for business decisions.
