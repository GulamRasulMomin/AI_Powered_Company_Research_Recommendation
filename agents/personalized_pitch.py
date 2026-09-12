from rich import print
from state import ResearchState
from llm import llm

def personalized_pitch_node(state: ResearchState) -> dict:
    """Generate a personalized pitch for CEO."""

    # print(f"[blue]Generating personalized pitch for CEO..............")

    company_name = state["company_name"]
    company_research = summarize_research(company_name, {**state["company_overview"], **state["business_information"]})
    challenges = state["challenges"]
    ai_opportunities = state["ai_opportunities"]

    prompt = f"""
    You are a senior AI business consultant meeting the CEO of the company.

    Company Name:
    {company_name}

    Company Research:
    {company_research}

    Identified Challenges:
    {challenges}

    AI Opportunities:
    {ai_opportunities}

    Create a detailed, personalized CEO pitch covering these three areas:

    1. WHY WE REACHED OUT
    Explain why this company is a strong candidate for AI transformation. Connect the company's business model, scale, recent developments, expansion plans, and identified challenges to the reason for reaching out.

    2. OPPORTUNITIES IDENTIFIED
    Explain the most important business opportunities identified from the research. Discuss opportunities related to operational efficiency, sales, customer experience, automation, analytics, cost reduction, revenue growth, and scalability where relevant.

    3. AI SOLUTIONS WE RECOMMEND
    Recommend specific AI solutions for the identified opportunities and challenges. For each solution, explain:

    * What the AI solution would do
    * Which business problem it addresses
    * How it would work at a high level
    * Expected business benefit
    * Why it is relevant to this specific company

    IMPORTANT RULES:

    * Make the pitch highly specific to {company_name}.
    * Use the provided research as the primary source.
    * Do not give generic AI recommendations.
    * Connect every AI solution to a specific challenge or opportunity.
    * Preserve important company facts, numbers, projects, locations, and business details.
    * Do not invent facts or claim unsupported problems.
    * You may make reasonable business inferences, but clearly present them as potential opportunities or risks.
    * Write in a persuasive, professional, CEO-level style.
    * Provide substantial detail; do not give short answers.
    * Avoid unnecessary repetition.
    * Return ONLY plain text.

    Use EXACTLY this structure:

    Why We Reached Out :

    Explanation...

    Opportunities We Identified :

    Explanation...

    Recommend AI Solutions :

    Explanation...

    """


    try:
        response = llm.invoke(prompt)
        personalized_pitch = response.content.strip()
    except Exception as e:
        print(f"[red]Error occurred in llm response in personalized pitch: {e}")
        personalized_pitch = ''
                
    
    return {"personalized_pitch": personalized_pitch}


def summarize_research(company_name: str, research_dict: dict) -> str:
    prompt = f"""
    You are a professional company research analyst.

    Company Name:
    {company_name}

    Research Information:
    {research_dict}

    Summarize the research into a concise but information-rich company profile.

    Include:
    - Company overview and business model
    - Industry and major offerings
    - Company scale and financial information
    - Geographic presence
    - Recent developments
    - Expansion plans
    - Important public information

    Rules:
    - Keep important facts, numbers, dates, project names, locations, and financial metrics.
    - Remove duplicate and irrelevant information.
    - Do not invent or assume information.
    - Keep the summary detailed but significantly shorter than the original research.
    - Maximum 370 words.
    - Return plain text only.
    """

    response = llm.invoke(prompt)
    return response.content.strip()