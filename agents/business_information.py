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


def business_information_node(state: ResearchState) -> dict:
    """Search information about a company's products, services, developments and expansion plans."""

    # print(f"[blue]Starting company business information research..........")

    company_name = state["company_name"]

    agent = create_agent(
        model=llm,
        tools=[tavily],
        system_prompt="""You are a company business research agent.

        When the user provides a company name:

        1. Search the web using Tavily.
        2. Research the company's:
        - major products
        - services and offerings
        - business portfolio
        - brands and business segments
        - recent developments and latest news
        - recent product or project launches
        - partnerships, acquisitions or investments
        - expansion plans
        - upcoming projects
        - new markets, cities or locations
        - official announcements and press releases
        3. Prefer recent and reliable sources.
        4. Prefer official company websites, investor relations pages,
        official press releases, stock exchange filings and reputable
        news sources whenever available.
        5. Do not invent information.
        6. Include dates when available.
        7. If a value cannot be found, say "Not available".
        8. Avoid repeating the same information across different fields.
        9. Return ONLY valid JSON.
        10. Do not return Markdown or code fences.
        11. Do not add any explanation outside the JSON.
        12. Aim for approximately 250-300 words for EACH field when
        sufficient information is available.

        Required JSON format:

        {
            "major_offerings": "string value",
            "recent_developments": "string value",
            "expansion_plans": "string value",
            "important_public_information": "string value"
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
        print(f"[red]Error occurred in llm response in company business information: {e}")
        research_content = {}
            

    return {"business_information": research_content}