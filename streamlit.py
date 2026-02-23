import streamlit as st
from dotenv import load_dotenv

# Import modular components
from src.data.career_data import CAREER_CATEGORIES
from src.utils.text_utils import as_markdown
from src.config import load_api_keys
from src.services.ai_service import (
    initialize_llm_and_tools,
    create_agent_with_tools,
    generate_career_insights,
    generate_market_analysis,
    generate_college_recommendations,
    generate_resume_feedback
)
from src.components.chat import create_chat_interface

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🎯 AI Career Guidance Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

def initialize_session_state():
    defaults = {
        "chat_history": [],
        "chat_messages": [],
        "career_insights": None,
        "market_analysis": None,
        "college_recommendations": None,
        "resume_feedback": None,
        "selected_career": None,
        "api_keys_validated": False,
        "active_tab": "career_insights",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def main():
    initialize_session_state()

    st.title("🎯 AI-Powered Career Guidance Platform")
    st.markdown(
        """
    **Discover your ideal career path with AI-powered insights, college recommendations, resume coaching, and real-time market analysis.**
    *Powered by Google Gemini, LangChain Agents, and SerpAPI | Focused on Indian Job Market & Education*
    """
    )

    api_keys = load_api_keys()
    with st.sidebar:
        st.header("🔧 Configuration")
        google_key = st.text_input(
            "🤖 Google Gemini API Key", value=api_keys["google_api_key"], type="password"
        )
        serpapi_key = st.text_input(
            "🔍 SerpAPI Key", value=api_keys["serpapi_key"], type="password"
        )

        if google_key and serpapi_key:
            st.success("✅ API keys configured")
            st.session_state.api_keys_validated = True
        else:
            st.warning("⚠️ Provide both API keys to enable live features")
            st.session_state.api_keys_validated = False

        st.markdown("---")
        st.markdown(
            """
        **How to use**
        1. Configure API keys above (or set in .env / Streamlit secrets)
        2. Choose career category & role
        3. Use tabs to explore:
           - 🧭 Career Insights
           - 📊 Market Analysis
           - 🎓 College Advisor
           - 📝 Resume Coach
        4. Use chat for personalized questions
        """
        )

        if st.button("🔄 Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if not st.session_state.api_keys_validated:
        st.info("👈 Please provide your Google Gemini and SerpAPI keys in the sidebar to get started.")
        st.subheader("🌟 Features")
        st.markdown(
            """
- 📊 Role analysis & learning roadmap
- 📈 Live market analysis (Indian job market)
- 🎓 College recommendations (Indian institutions)
- 📝 AI-powered resume coaching
- 💬 Interactive career advisor chat
- 🏢 Multi-industry coverage (Tech, Healthcare, Business, Content)
"""
        )
        return

    llm, tools = initialize_llm_and_tools(google_key, serpapi_key)
    if not llm or not tools:
        st.error("❌ Failed to initialize AI components. Check your API keys and network.")
        return

    agent_executor = create_agent_with_tools(llm, tools)
    if agent_executor is None:
        st.error("❌ Agent initialization failed.")
        return

    st.subheader("🎯 Select Your Career Interest")
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_category = st.selectbox("📁 Choose a career category:", list(CAREER_CATEGORIES.keys()))
    with col2:
        selected_subcareer = st.selectbox("🎯 Choose specific career:", CAREER_CATEGORIES[selected_category])

    # Tab interface for different features
    tab1, tab2, tab3, tab4 = st.tabs(["🧭 Career Insights", "📊 Market Analysis", "🎓 College Advisor", "📝 Resume Coach"])

    with tab1:
        st.markdown("### 🧭 Career Insights & Learning Roadmap")
        if st.button("🚀 Generate Career Insights", key="btn_career_insights", use_container_width=True):
            st.session_state.selected_career = f"{selected_category} → {selected_subcareer}"
            career_insights = generate_career_insights(selected_category, selected_subcareer, llm)
            st.session_state.career_insights = career_insights
            st.markdown(as_markdown(career_insights))
        elif st.session_state.career_insights:
            st.info(f"📋 Showing cached results for: **{st.session_state.selected_career}**")
            st.markdown(as_markdown(st.session_state.career_insights))

    with tab2:
        st.markdown("### 📊 Live Market Analysis")
        if st.button("📈 Fetch Market Data", key="btn_market_analysis", use_container_width=True):
            st.session_state.selected_career = f"{selected_category} → {selected_subcareer}"
            market_analysis = generate_market_analysis(selected_subcareer, llm)
            st.session_state.market_analysis = market_analysis
            st.markdown(as_markdown(market_analysis))
        elif st.session_state.market_analysis:
            st.info(f"📋 Showing cached results for: **{st.session_state.selected_career}**")
            st.markdown(as_markdown(st.session_state.market_analysis))

    with tab3:
        st.markdown("### 🎓 College & University Recommendations")
        st.markdown("*Get personalized recommendations for Indian colleges and universities*")
        if st.button("🏛️ Get College Recommendations", key="btn_college_recs", use_container_width=True):
            st.session_state.selected_career = f"{selected_category} → {selected_subcareer}"
            college_recommendations = generate_college_recommendations(selected_subcareer, llm)
            st.session_state.college_recommendations = college_recommendations
            st.markdown(as_markdown(college_recommendations))
        elif st.session_state.college_recommendations:
            st.info(f"📋 Showing cached results for: **{st.session_state.selected_career}**")
            st.markdown(as_markdown(st.session_state.college_recommendations))

    with tab4:
        st.markdown("### 📝 Resume Coach & Feedback")
        st.markdown("*Get AI-powered feedback on your resume*")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["📄 Upload Resume File", "✍️ Paste Resume Text"],
            horizontal=True,
            key="resume_input_method"
        )
        
        resume_text = ""
        
        if input_method == "📄 Upload Resume File":
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF, DOCX, or TXT)",
                type=["pdf", "docx", "doc", "txt"],
                key="resume_file_uploader",
                help="Supported formats: PDF, Word (DOCX/DOC), and plain text files"
            )
            
            if uploaded_file is not None:
                try:
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    
                    if file_extension == 'txt':
                        resume_text = uploaded_file.read().decode('utf-8')
                        st.success(f"✅ Loaded {len(resume_text)} characters from {uploaded_file.name}")
                    
                    elif file_extension == 'pdf':
                        try:
                            import PyPDF2
                            from io import BytesIO
                            
                            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                            resume_text = ""
                            for page in pdf_reader.pages:
                                resume_text += page.extract_text() + "\n"
                            st.success(f"✅ Extracted {len(resume_text)} characters from PDF")
                        except ImportError:
                            st.error("❌ PyPDF2 not installed. Install it with: pip install PyPDF2")
                        except Exception as e:
                            st.error(f"❌ Error reading PDF: {e}")
                    
                    elif file_extension in ['docx', 'doc']:
                        try:
                            import docx
                            from io import BytesIO
                            
                            doc = docx.Document(BytesIO(uploaded_file.read()))
                            resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                            st.success(f"✅ Extracted {len(resume_text)} characters from Word document")
                        except ImportError:
                            st.error("❌ python-docx not installed. Install it with: pip install python-docx")
                        except Exception as e:
                            st.error(f"❌ Error reading Word document: {e}")
                    
                    # Show preview
                    if resume_text:
                        with st.expander("📄 Preview extracted text"):
                            st.text_area("Resume content:", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200, disabled=True)
                            
                except Exception as e:
                    st.error(f"❌ Error processing file: {e}")
        
        else:  # Paste text option
            resume_text = st.text_area(
                "Paste your resume content here:",
                height=300,
                placeholder="Copy and paste your resume text here...\n\nInclude all sections: Summary, Experience, Education, Skills, etc.",
                key="resume_text_input"
            )
        
        target_role_input = st.text_input(
            "Target Role (optional - uses selected career if empty):",
            placeholder="e.g., Senior Data Scientist",
            key="target_role_input"
        )
        
        if st.button("🔍 Analyze Resume", key="btn_resume_analysis", use_container_width=True):
            if not resume_text or len(resume_text.strip()) < 100:
                st.warning("⚠️ Please provide your resume content (at least 100 characters)")
            else:
                target_role = target_role_input if target_role_input else selected_subcareer
                resume_feedback = generate_resume_feedback(resume_text, target_role, llm)
                st.session_state.resume_feedback = resume_feedback
                st.markdown(as_markdown(resume_feedback))
        elif st.session_state.resume_feedback:
            st.info("📋 Showing previous resume analysis")
            st.markdown(as_markdown(st.session_state.resume_feedback))

    st.markdown("---")
    create_chat_interface(agent_executor)

    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666; padding: 16px;'>
        🎯 <strong>AI-Powered Career Guidance Platform</strong> — Built with LangChain & Gemini | 🇮🇳 Indian Market Focus
    </div>
    """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
