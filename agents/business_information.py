import json
from web_search import web_search
from rich import print
from state import ResearchState
from llm import llm

def business_information_node(state: ResearchState) -> dict:
    """Search and scrape business information about a company."""

    # print(f"[blue]Starting business information research..........")

    company_name = state["company_name"]

    queries = [
        f"{company_name} products services offerings portfolio",
        f"{company_name} recent developments news announcements",
        f"{company_name} expansion plans upcoming projects launch",
        f"{company_name} press release official announcement",
    ]

    research_data = ''

    for query in queries:
        try:
            search_results = web_search(query)

            sources = []

            for result in search_results:
                sources.append(result["content"])

            research_data += "\n".join(sources)
            
        except Exception as e:
                   print(f"[red]Error occurred while researching '{query}': {e}")

    prompt = f"""
    You are a professional company research analyst.

    Company Name:
    {company_name}

    Research information collected from multiple web searches:

    Your task is to organize and summarize this information into a single
    JSON object with exactly four top-level keys:

    - major_offerings
    - recent_developments
    - expansion_plans
    - important_public_information

    IMPORTANT OUTPUT RULES:

    1. Return ONLY valid JSON.
    2. Do not return Markdown or code fences.
    3. Do not add any explanation outside the JSON.
    4. Each of the four fields MUST contain a STRING value.
    5. Do NOT use nested objects, arrays, lists, or dictionaries as values.
    6. Combine related information into a clear and detailed paragraph for each field.
    7. Remove duplicate and irrelevant information.
    8. Do not hallucinate or invent information.
    9. Use only information available in the research text.
    10. Preserve important numbers, dates, names, project names, financial figures,
        investments, partnerships, locations, and other important metrics.
    11. If information for a field is unavailable, use "Information not available."
    12. Do not repeat the same information unnecessarily across different fields.
    13. If conflicting information exists, mention the conflict briefly within the
        relevant string.
    14. Each field should contain a detailed and informative summary.
    15. Do not create any additional keys.
    16. Aim for approximately 250-280 words for EACH field when sufficient
        information is available.
    17. Preserve as much relevant information as possible instead of overly
        compressing the research results.
    18. Clearly distinguish between confirmed information and future plans or
        potential opportunities.

    CONTENT GUIDELINES:

    major_offerings:
    Include the company's major products, services, solutions, brands,
    business offerings, and major business segments.

    Focus on:
    - Main products and services
    - Major brands
    - Product categories
    - Business segments
    - Residential/commercial offerings
    - Luxury, premium, affordable, or other offerings
    - Technology or digital offerings
    - Specialized services
    - Major projects or solutions
    - Target customer segments related to the offerings

    recent_developments:
    Include important developments and events that have occurred recently.

    Focus on:
    - Recent announcements
    - New projects and project launches
    - New products or services
    - Recent investments and funding
    - Strategic partnerships
    - Acquisitions or joint ventures
    - Leadership changes
    - Financial developments
    - New contracts or major deals
    - Technology implementations
    - Awards and recognition
    - Sustainability initiatives
    - Major business achievements
    - Other significant recent developments

    Always include the date or year of a development when available.

    expansion_plans:
    Include the company's current, planned, or announced expansion
    and growth initiatives.

    Focus on:
    - New cities
    - New countries
    - New markets
    - New projects
    - New offices
    - Geographic expansion
    - Capacity expansion
    - Land acquisition
    - New business segments
    - Planned investments
    - Strategic growth initiatives
    - International expansion
    - Future projects
    - Announced expansion targets

    Clearly distinguish between confirmed/planned expansion and
    potential or explored opportunities.

    Do not treat an explored opportunity as a confirmed expansion.

    important_public_information:
    Include other important publicly available information about the company
    that does not clearly belong to the other three categories.

    Focus on:
    - Public company information
    - Stock exchange information
    - Regulatory information
    - Public financial information
    - Ownership information
    - Management information
    - Public filings
    - Important awards and recognition
    - Sustainability and ESG information
    - Corporate governance
    - Major subsidiaries
    - Strategic partnerships
    - Publicly announced investments
    - Important company milestones
    - Other significant information useful for company research

    The final JSON MUST have exactly this format:

    {{
        "major_offerings": "string value",
        "recent_developments": "string value",
        "expansion_plans": "string value",
        "important_public_information": "string value"
    }}

    Research Text:
    {research_data}
    """  
      
    try:
        response = llm.invoke(prompt)
        research_content = json.loads(response.content.strip())
    except Exception as e:
        print(f"[red]Error occurred in llm response in business information: {e}")
        research_content = {}
            

    return {"business_information": research_content}
