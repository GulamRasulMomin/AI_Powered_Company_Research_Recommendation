import json
import os

import streamlit as st
from graph import app as research_app


st.set_page_config(
    page_title="Research Intelligence Studio",
    page_icon="RI",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#16232d; --muted:#60717b; --paper:#f6f5f0; --line:#dce3df; --teal:#167d76; --deep:#0d5c59; --coral:#e5795f; }
    .stApp { background:radial-gradient(circle at 90% 0%, #e8f1ec 0, transparent 34rem), var(--paper); color:var(--ink); font-family:'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { background:#102c32; border-right:0; }
    [data-testid="stSidebar"] * { color:#eaf3ee; }
    [data-testid="stSidebar"] .stCaption { color:#a9c5bd; }
    h1,h2,h3 { font-family:'Space Grotesk', sans-serif; letter-spacing:0; }
    h1 { font-size:clamp(2.4rem, 5vw, 4.7rem); line-height:.98; max-width:820px; }
    .eyebrow { color:var(--coral); font-size:.78rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; margin-bottom:.8rem; }
    .lede { color:var(--muted); font-size:1.08rem; max-width:680px; line-height:1.6; }
    .metric-strip { border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:1rem 0; margin:2rem 0 2.5rem; }
    .metric-label { color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }
    .metric-value { color:var(--deep); font-family:'Space Grotesk'; font-size:1.4rem; font-weight:700; }
    .report-intro { background:var(--deep); border-radius:8px; color:#f4faf5; padding:1.3rem 1.5rem; margin:1rem 0 1.4rem; }
    .report-intro h2 { color:#f4faf5; margin:0 0 .25rem; }
    .report-intro p { color:#c8dfd7; margin:0; }
    div[data-testid="stForm"] { background:white; border:1px solid var(--line); border-radius:8px; padding:1.25rem; }
    div[data-testid="stForm"] button[kind="primary"] { background:var(--coral); border:0; color:white; font-weight:700; }
    [data-baseweb="tab"] { color:#53656d !important; font-weight:600; }
    [data-baseweb="tab"] p { color:#53656d !important; }
    [data-baseweb="tab"][aria-selected="true"], [data-baseweb="tab"][aria-selected="true"] p { color:var(--coral) !important; }
    [data-baseweb="tab-highlight"] { background-color:var(--coral) !important; }
    [data-testid="stExpander"] { background:white; border:1px solid var(--line); border-radius:8px; }
    [data-testid="stExpander"] details summary { background:#edf3f0; color:var(--ink) !important; }
    [data-testid="stExpander"] details summary p,
    [data-testid="stExpander"] details summary span { color:var(--ink) !important; font-weight:600; }
    [data-testid="stExpander"] details summary:hover { background:#e1ece8; }
    [data-testid="stExpander"] details div[data-testid="stExpanderDetails"] { background:white; color:var(--ink); }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_section(title: str, content: object) -> None:
    st.subheader(title)
    if isinstance(content, dict):
        for label, value in content.items():
            with st.expander(label.replace("_", " ").title(), expanded=True):
                st.write(value or "Information not available.")
    else:
        st.write(content or "Information not available.")


def render_report(result: dict, company_name: str) -> None:
    st.markdown(
        f"""
        <div class="report-intro">
            <h2>{company_name} intelligence report</h2>
            <p>Research, business context, risks, and practical AI opportunities.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    profile, intelligence = st.tabs(["Company profile", "Business intelligence"])
    with profile:
        render_section("Company overview", result.get("company_overview", {}))
        render_section("Business information", result.get("business_information", {}))
    with intelligence:
        challenges, opportunities, pitch = st.tabs(
            ["Potential challenges", "AI opportunities", "Personalized pitch"]
        )
        with challenges:
            render_section("Potential challenges", result.get("challenges", {}))
        with opportunities:
            render_section("AI opportunities", result.get("ai_opportunities", {}))
        with pitch:
            st.subheader("CEO-ready pitch")
            st.write(result.get("personalized_pitch") or "No pitch was generated.")



st.title("Know the company before you pitch it.")
st.markdown(
    '<p class="lede">Turn a company name into a structured intelligence brief: what is happening now, where friction may exist, and where AI can create leverage.</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="metric-strip"><span class="metric-label">One input</span>&nbsp;&nbsp; <span class="metric-value">Five perspectives</span>&nbsp;&nbsp;&nbsp;&nbsp; <span class="metric-label">Profile · challenges · opportunities · pitch</span></div>',
    unsafe_allow_html=True,
)

with st.form("research_form"):
    company_name = st.text_input(
        "Company name",
        placeholder="Try Puravankara, Sobha, or Brigade Group",
    )
    submitted = st.form_submit_button(
        "Generate intelligence report",
        type="primary",
        use_container_width=True,
    )

if submitted:
    company_name = company_name.strip()
    if not company_name:
        st.warning("Enter a company name to begin the research.")
    elif not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("Add GROQ_API_KEY and TAVILY_API_KEY to your .env file before running research.")
    else:
        with st.status(f"Researching {company_name}...", expanded=True) as status:
            try:
                

                st.write("Searching public sources and building the company profile...")
                result = research_app.invoke({"company_name": company_name})
                status.update(label="Report ready", state="complete", expanded=False)
                st.session_state["research_result"] = result
                st.session_state["research_company"] = company_name
            except Exception as error:
                status.update(label="Research failed", state="error")
                st.error(f"The research pipeline could not complete: {error}")

if "research_result" in st.session_state:
    render_report(
        st.session_state["research_result"],
        st.session_state["research_company"],
    )