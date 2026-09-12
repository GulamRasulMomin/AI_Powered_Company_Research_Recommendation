import json
from rich import print
from state import ResearchState
from llm import llm

def ai_opportunities_node(state: ResearchState) -> dict:
    """analyze AI opportunities for a company."""

    # print(f"[blue]Generating AI Opportunities............")

    company_name = state["company_name"]
    company_data = {**state["business_information"], **state["challenges"]}

    prompt = f"""
    You are a professional AI business consultant.

    Company Name:
    {company_name}

    Research and Identified Challenges:
    {company_data}

    Suggest practical, company-specific AI opportunities based on the research and challenges.

    Identify opportunities across:

    * AI Automation
    * Customer engagement
    * Sales
    * Operations
    * Analytics
    * Document processing

    IMPORTANT RULES:

    1. Return ONLY valid JSON.
    2. Use exactly these six categories.
    3. Each value MUST be a detailed STRING.
    4. Do not use arrays, lists, or nested objects.
    5. Do not give generic AI suggestions.
    6. Every opportunity must be directly connected to the company's business, operations, or identified challenges.
    7. Explain the AI solution and the business problem it solves.
    8. Prioritize realistic and implementable AI use cases.
    9. Do not invent company processes or data that are not supported by the research.
    10. Mention expected business impact where possible.

    FINAL FORMAT:

    {{
    "automation": "Company-specific AI automation opportunities and their business impact.",
    "customer_engagement": "AI opportunities for improving customer communication, support, and engagement.",
    "sales": "AI opportunities for lead generation, qualification, conversion, forecasting, and sales optimization.",
    "operations": "AI opportunities for improving project execution, resource management, monitoring, and operational efficiency.",
    "analytics": "AI opportunities for forecasting, decision-making, risk detection, performance analysis, and business intelligence.",
    "document_processing": "AI opportunities for processing contracts, legal documents, project documents, reports, invoices, and other relevant documents."
    }}
    """


    try:
        response = llm.invoke(prompt)
        opportunities_content = json.loads(response.content.strip())
    except Exception as e:
        print(f"[red]Error occurred in llm response in AI opportunities: {e}")
        opportunities_content = {}
                
    
    return {"ai_opportunities": opportunities_content}
