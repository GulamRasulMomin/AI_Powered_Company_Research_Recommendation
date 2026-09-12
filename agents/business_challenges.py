import json
from rich import print
from state import ResearchState
from llm import llm


def business_challenges_node(state: ResearchState) -> dict:
    """analyze business challenges of a company."""

    # print(f"[blue]analysis business challenges..............")

    company_name = state["company_name"]
    research_data = {**state["company_overview"], **state["business_information"]}

    prompt = f"""
    You are a professional business research analyst.

    Company Name:
    {company_name}

    Research Information:
    {research_data}

    Identify potential challenges in exactly these four categories:

    * possible_challenges
    * operational_bottlenecks
    * sales_challenges
    * customer_experience_challenges

    OUTPUT RULES:

    1. Return ONLY valid JSON.
    2. Use exactly these four keys.
    3. Each value MUST be a detailed STRING.
    4. Do not use arrays, lists, or nested objects.
    5. Use only the research information and reasonable business inferences.
    6. Do not hallucinate or claim unsupported problems as facts.
    7. Clearly indicate inferred challenges as "potential" or "may".
    8. Explain why each challenge could occur and its possible business impact.
    9. Avoid repeating the same challenge across categories.
    10. Preserve important numbers, dates, projects, locations, and metrics when relevant.
    11. If information is insufficient, state that clearly.

    FOCUS:

    possible_challenges:
    Strategic, financial, market, competition, expansion, regulatory, workforce, and growth challenges.

    operational_bottlenecks:
    Project execution, construction, procurement, supply chain, resource allocation, quality, technology, coordination, and delivery challenges.

    sales_challenges:
    Lead generation, conversion, competition, pricing, inventory, collections, customer acquisition, market demand, and NRI sales challenges.

    customer_experience_challenges:
    Communication, construction updates, delivery, quality, handover, after-sales service, complaints, digital support, and consistency across locations.

    Use this reasoning:
    Research Evidence → Potential Challenge → Why It Matters → Business Impact

    FINAL FORMAT:

    {{
    "possible_challenges": "string",
    "operational_bottlenecks": "string",
    "sales_challenges": "string",
    "customer_experience_challenges": "string"
    }}"""


    try:
        response = llm.invoke(prompt)
        challenges_content = json.loads(response.content.strip())
    except Exception as e:
        print(f"[red]Error occurred in llm response in business challenges: {e}")
        challenges_content = {}
                
    
    return {"challenges": challenges_content}
