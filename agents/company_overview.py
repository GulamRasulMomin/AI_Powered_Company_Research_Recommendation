import json
from web_search import web_search
from rich import print
from state import ResearchState
from llm import llm


def company_overview_node(state: ResearchState) -> dict:
    """Search and scrape information about a company."""

    # print(f"[blue]Starting company overview research..........")

    company_name = state["company_name"]

    queries = [
        f"{company_name} company profile overview",
        f"{company_name} industry sector",
        f"{company_name} revenue annual turnover employees size",
        f"{company_name} cities locations operations presence",
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

    - company_information
    - industry
    - scale
    - geographic_presence

    IMPORTANT OUTPUT RULES:

    1. Return ONLY valid JSON.
    2. Do not return Markdown or code fences.
    3. Do not add any explanation outside the JSON.
    4. Each of the four fields MUST contain a STRING value.
    5. Do NOT use nested objects, arrays, lists, or dictionaries as values.
    6. Combine related information into a clear paragraph for each field.
    7. Remove duplicate and irrelevant information.
    8. Do not hallucinate or invent information.
    9. Use only information available in the research text.
    10. Preserve important numbers, dates, names, financial figures, and metrics.
    11. If information for a field is unavailable, use "Information not available."
    12. Do not repeat the same information unnecessarily across different fields.
    13. If conflicting information exists, mention the conflict briefly within the
        relevant string.
    14. Each field should contain a concise but informative paragraph.
    15. Do not create any additional keys.
    16. Aim for approximately 250-280 words for EACH field when sufficient
        information is available.

    CONTENT GUIDELINES:

    company_information:
    Include company identity, founding/incorporation year, headquarters,
    company type, stock listing, major brands, subsidiaries, key people,
    and general company description.

    industry:
    Include industry, sector, business model, major business segments,
    products/services, target customers, and competitive positioning.

    scale:
    Include employees, revenue, annual turnover, market capitalization,
    completed area, development pipeline, land bank, number of projects,
    sales, EBITDA, profit, and other important company-size or financial
    metrics when available.

    geographic_presence:
    Include headquarters location, countries, states, cities, offices,
    project locations, domestic presence, and international operations.

    The final JSON MUST have exactly this format:

    {{
        "company_information": "string value",
        "industry": "string value",
        "scale": "string value",
        "geographic_presence": "string value"
    }}

    Research Text:
    {research_data}"""
    
      
    try:
        response = llm.invoke(prompt)
        research_content = json.loads(response.content.strip())
    except Exception as e:
        print(f"[red]Error occurred in llm response in company overview: {e}")
        research_content = {}
            

    return {"company_overview": research_content}
