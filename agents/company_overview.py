import json
from state import ResearchState
from llm import llm
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilySearch(
    max_results=5,
    topic="general"
)


def company_overview_node(state: ResearchState) -> dict:
    """Search information about a company."""

    # print(f"[blue]Starting company overview research..........")

    company_name = state["company_name"]

    agent = create_agent(
        model=llm,
        tools=[tavily],
        system_prompt="""You are a company research agent.

        When the user provides a company name:

        1. Search the web using Tavily.
        2. Research the company's:
        - company profile/overview
        - industry sector
        - annual revenue or turnover
        - employee size
        - cities and geographic locations
        - operational presence
        3. Prefer recent and reliable sources.
        4. Do not invent information.
        5. If a value cannot be found, say "Not available".
        6. Return ONLY valid JSON.
        7. Do not return Markdown or code fences.
        8. Do not add any explanation outside the JSON.
        9. Aim for approximately 250-300 words for EACH field when sufficient information is available.

        Required JSON format:

        {
            "company_information": "string value",
            "industry": "string value",
            "scale": "string value",
            "geographic_presence": "string value"
        }
        """
        )

      
    try:
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": company_name
                }
            ]
        })
        research_content = json.loads(result["messages"][-1].content.strip())
    except Exception as e:
        print(f"[red]Error occurred in llm response in company overview: {e}")
        research_content = {}
            

    return {"company_overview": research_content}

