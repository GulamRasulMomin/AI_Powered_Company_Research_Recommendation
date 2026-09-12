from langgraph.graph import StateGraph , START , END
from state import ResearchState
from agents.company_overview import company_overview_node
from agents.business_information import business_information_node
from agents.business_challenges import business_challenges_node
from agents.ai_opportunities import ai_opportunities_node
from agents.personalized_pitch import personalized_pitch_node
from rich import print

graph = StateGraph(ResearchState)

graph.add_node("company_overview", company_overview_node)
graph.add_node("business_information", business_information_node)
graph.add_node("challenges", business_challenges_node)
graph.add_node("ai_opportunities", ai_opportunities_node)
graph.add_node("personalized_pitch", personalized_pitch_node)

graph.add_edge(START,"company_overview")
graph.add_edge(START, "business_information")
graph.add_edge("company_overview", "challenges")
graph.add_edge("business_information", "challenges")
graph.add_edge("challenges", "ai_opportunities")
graph.add_edge("ai_opportunities", "personalized_pitch")
graph.add_edge("personalized_pitch", END)

app = graph.compile()

if __name__ == "__main__":    
    result = app.invoke({
        "company_name" :"Puravankara"
    })

    print("Company Overview : \n",result['company_overview'])
    print("Business Information : \n",result['business_information'])
    print("Business Challenges : \n",result['challenges'])
    print("AI Opportunities : \n",result['ai_opportunities'])
    print("Personalized Pitch : \n",result['personalized_pitch'])