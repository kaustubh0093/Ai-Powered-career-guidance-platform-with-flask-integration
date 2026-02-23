from typing import List, Tuple, Optional
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool
from langchain.agents import initialize_agent, AgentType

@st.cache_resource
def initialize_llm_and_tools(google_api_key: str, serpapi_key: str) -> Tuple[Optional[ChatGoogleGenerativeAI], Optional[List[Tool]]]:
    try:
        if not google_api_key:
            raise ValueError("Google API key is required.")
        if not serpapi_key:
            raise ValueError("SerpAPI key is required.")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.1,
        )

        search = SerpAPIWrapper(
            serpapi_api_key=serpapi_key,
            params={"engine": "google", "google_domain": "google.com", "gl": "in", "hl": "en"},
        )

        search_tool = Tool(
            name="web_search",
            description="Use to search the web for job market trends, salaries, companies, Indian colleges, and live data.",
            func=search.run,
        )

        return llm, [search_tool]
    except Exception as e:
        st.error(f"❌ Error initializing LLM/tools: {e}")
        return None, None

def create_agent_with_tools(llm, tools: List[Tool]):
    try:
        agent_executor = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )
        return agent_executor
    except Exception as e:
        st.error(f"❌ Error creating agent: {e}")
        return None

def generate_career_insights(category: str, subcareer: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        career_prompt = f"""
Generate a comprehensive career analysis for:

**Category**: {category}
**Career**: {subcareer}

Provide structured markdown that includes:
1) Career Overview (role, responsibilities, daily tasks)
2) Required Skills & Tools (technical + soft skills)
3) Learning Roadmap (beginner → intermediate → advanced)
4) Career Progression Path (roles & salary bands in India)
5) Future Outlook & trends
6) Suggested Resources (courses, books, certifications)
7) Quick Reference Summary (salary ranges in INR, demand in India, remote options)

Keep the output practical, actionable, and formatted in markdown. Focus on the Indian job market context.
"""

        with st.spinner("🧭 Generating career insights..."):
            output = llm.invoke(career_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating career insights: {e}")
        return f"❌ Unable to generate career insights. Error: {e}"

def generate_market_analysis(subcareer: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        market_prompt = f"""
Search the web (live) and analyze the current job market in India for the role: "{subcareer}".

Please include:
- Current job demand and hiring trends in India (last 12 months)
- Typical salary ranges in INR (entry / mid / senior level)
- Top Indian companies hiring and industry sectors
- Major hiring cities in India (Bangalore, Mumbai, Delhi, Hyderabad, Pune, etc.)
- Skills in highest demand for this role in India
- Remote work availability and trends in India
- Short list of sources (urls or site names) used

Return a concise, well-structured markdown analysis with bullet points and a small summary table.
Focus specifically on the Indian job market.
"""

        with st.spinner("📊 Fetching live market data..."):
            output = llm.invoke(market_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating market analysis: {e}")
        return f"❌ Unable to fetch market analysis. Error: {e}"

def generate_college_recommendations(subcareer: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        college_prompt = f"""
As a college advisor, provide detailed recommendations for pursuing a career in "{subcareer}" in India.

Please include:

1) **Recommended Educational Paths**:
   - Degree programs (BTech, BSc, BA, MBA, MSc, etc.)
   - Specializations to focus on
   - Duration and typical eligibility

2) **Top Indian Colleges/Universities** (at least 10-15):
   - IITs, NITs, IIITs, and other premier institutes
   - State universities and private colleges
   - Include admission processes (JEE, GATE, CAT, etc.)
   - Approximate fees and placement records where known

3) **Alternative Education Paths**:
   - Online courses and certifications
   - Bootcamps and vocational training
   - Diploma programs

4) **Entrance Exams**:
   - Required entrance exams for admission
   - Preparation tips and resources

5) **Scholarships & Financial Aid**:
   - Government scholarships available
   - Merit-based and need-based options

6) **Additional Tips**:
   - Best states/cities for education in this field
   - Industry certifications to pursue alongside degree
   - Internship opportunities during education

Format the response in clear markdown with sections, bullet points, and tables where appropriate.
Focus exclusively on Indian institutions and the Indian education system.
"""

        with st.spinner("🎓 Generating college recommendations..."):
            output = llm.invoke(college_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating college recommendations: {e}")
        return f"❌ Unable to generate college recommendations. Error: {e}"

def generate_resume_feedback(resume_text: str, target_role: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        resume_prompt = f"""
As an expert resume coach, analyze the following resume for the target role: "{target_role}"

**Resume Content**:
{resume_text}

Provide comprehensive feedback in the following structure:

1) **Overall Assessment** (Score: X/10):
   - Brief summary of strengths and weaknesses
   - First impression rating

2) **Content Analysis**:
   - Relevance to target role
   - Key achievements and quantifiable results
   - Skills alignment with job requirements
   - Missing critical information

3) **Format & Structure**:
   - Layout and readability assessment
   - Section organization
   - Length appropriateness

4) **Specific Improvements Needed**:
   - What to add (skills, experiences, keywords)
   - What to remove or reduce
   - How to rephrase key sections
   - ATS (Applicant Tracking System) optimization tips

5) **Section-by-Section Feedback**:
   - Summary/Objective
   - Work Experience
   - Education
   - Skills
   - Projects/Certifications

6) **Action Items** (Priority-ordered):
   - Top 5-7 changes to make immediately
   - Keywords to include for ATS
   - Formatting improvements

7) **Example Improvements**:
   - Before/After examples for 2-3 bullet points
   - Better ways to phrase achievements

8) **Industry-Specific Tips**:
   - Tailored advice for the Indian job market
   - Cultural considerations for Indian recruiters

Be constructive, specific, and actionable. Use markdown formatting with clear sections.
"""

        with st.spinner("📝 Analyzing resume..."):
            output = llm.invoke(resume_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating resume feedback: {e}")
        return f"❌ Unable to analyze resume. Error: {e}"
