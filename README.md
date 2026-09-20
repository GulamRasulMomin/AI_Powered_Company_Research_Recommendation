# AI-Powered Company Research Recommendation

I developed an AI-powered research agent that takes a company name as input, searches publicly available information, analyzes the company's business, identifies potential challenges, finds company-specific AI opportunities, and generates a personalized CEO-ready pitch.

Before approaching a company for an AI solution, we need to understand its business, current activities, challenges, and possible areas where AI can provide value.
The main problems were:
   -	Manually researching a company takes a lot of time.
   -	Information is scattered across different web sources.
   -	Generic AI recommendations are not useful for a specific company.
   -	It is difficult to identify business challenges from raw information.
   -	A sales team needs a personalized pitch based on the company's actual business situation.

I solved this problem by creating an AI research and recommendation workflow using LangGraph. When the user enters a company name, it generate :

- Company overview
- Current business information
- Potential business challenges
- Practical AI opportunities
- Personalized, CEO-ready pitch
- Interactive report sections in a Streamlit interface

## Tech Stack

- Streamlit – user interface
- LangGraph – workflow orchestration
-	LangChain – LLM integration
-	LLM – Groq hosted  model : openai/gpt-oss-120b
-	Tavily – web search


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

The final system allows users to enter company name. The system researches the company and can identify its real-estate operations, offerings, expansion activities, and publicly available business information.

It then analyzes this information to identify possible challenges and recommends AI solutions such as AI-powered customer engagement, sales lead qualification, document processing, or operational analytics, depending on the company's specific situation.

Finally, it generates a CEO-ready pitch explaining why the company was selected, which opportunities were identified, and how AI could address them.

The LangGraph workflow starts the company overview and business information research in parallel. It then uses those results to generate:

1. Potential business challenges
2. AI opportunities
3. A personalized pitch

The language model is configured in `llm.py` as `openai/gpt-oss-120b` through Groq and Web search through Tavily.

## Project Demo video link

https://drive.google.com/file/d/1AsDuWvfnOD9eRJooW0iXEolLVn6kiquz/view?usp=sharing
