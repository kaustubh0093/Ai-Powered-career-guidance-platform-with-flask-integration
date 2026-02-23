from flask import Blueprint, request, jsonify
from backend.services.ai_service import (
    initialize_llm_and_tools,
    generate_career_insights,
    generate_market_analysis,
    generate_college_recommendations,
    generate_resume_feedback,
    create_agent_with_tools,
    search_jobs
)
from backend.data.career_data import CAREER_CATEGORIES
from backend.utils.text_utils import as_markdown
from backend.utils.file_utils import extract_text_from_file
from backend.config import Config
import logging

# Set up logging
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Cache for LLM and Agent (Global for simplicity in this prototype)
_llm = None
_agent = None

def get_ai_components():
    global _llm, _agent
    if _llm is None:
        if not Config.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY is missing in Config")
        if not Config.SERPAPI_KEY:
            logger.error("SERPAPI_KEY is missing in Config")
            
        _llm, tools = initialize_llm_and_tools(Config.GOOGLE_API_KEY, Config.SERPAPI_KEY)
        if _llm and tools:
            _agent = create_agent_with_tools(_llm, tools)
    return _llm, _agent

@api_bp.route('/careers', methods=['GET'])
def get_careers():
    """
    Get all career categories and roles
    ---
    responses:
      200:
        description: A dictionary of career categories and their transition roles
    """
    return jsonify(CAREER_CATEGORIES)

@api_bp.route('/chat', methods=['POST'])
def chat():
    """
    Interactive AI Career Advisor Chat
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
              example: "How do I become a Data Scientist in India?"
            history:
              type: array
              items:
                type: object
    responses:
      200:
        description: AI response to the message
      500:
        description: API keys or AI component error
    """
    data = request.json
    message = data.get('message')
    history = data.get('history', [])
    
    llm, agent = get_ai_components()
    if not agent:
        return jsonify({"error": "AI components not initialized. Check API keys."}), 500
    
    try:
        response = agent.invoke({"input": message})
        answer = response.get("output", "I'm sorry, I couldn't process that.")
        return jsonify({"answer": as_markdown(answer)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/career-insights', methods=['POST'])
def career_insights():
    """
    Generate professional career insights and learning roadmap
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            category:
              type: string
            subcareer:
              type: string
    responses:
      200:
        description: Detailed career analysis in markdown
    """
    data = request.json
    category = data.get('category')
    subcareer = data.get('subcareer')
    
    llm, _ = get_ai_components()
    if not llm:
        return jsonify({"error": "LLM not initialized"}), 500
    
    result = generate_career_insights(category, subcareer, llm)
    return jsonify({"result": as_markdown(result)})

@api_bp.route('/market-analysis', methods=['POST'])
def market_analysis():
    """
    Analyze the current job market in India for a specific role
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            subcareer:
              type: string
    responses:
      200:
        description: Market analysis summary with salaries and trends
    """
    data = request.json
    subcareer = data.get('subcareer')
    
    llm, _ = get_ai_components()
    if not llm:
        return jsonify({"error": "LLM not initialized"}), 500
    
    result = generate_market_analysis(subcareer, llm)
    return jsonify({"result": as_markdown(result)})

@api_bp.route('/college-recommendations', methods=['POST'])
def college_recommendations():
    """
    Get personalized recommendations for Indian colleges and entrance exams
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            subcareer:
              type: string
    responses:
      200:
        description: List of colleges, paths, and exams
    """
    data = request.json
    subcareer = data.get('subcareer')
    
    llm, _ = get_ai_components()
    if not llm:
        return jsonify({"error": "LLM not initialized"}), 500
    
    result = generate_college_recommendations(subcareer, llm)
    return jsonify({"result": as_markdown(result)})

@api_bp.route('/resume-analysis', methods=['POST'])
def resume_analysis():
    """
    AI-powered resume coach and feedback analysis
    ---
    parameters:
      - name: resume_text
        in: formData
        type: string
        description: Full text of the resume
      - name: target_role
        in: formData
        type: string
      - name: file
        in: formData
        type: file
        description: Resume file (PDF, DOCX, TXT)
    responses:
      200:
        description: Constructive feedback and ATS optimization tips
    """
    # Handle both text and file upload
    resume_text = request.form.get('resume_text', '')
    target_role = request.form.get('target_role', '')
    
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            resume_text = extract_text_from_file(file)
    
    if not resume_text:
        return jsonify({"error": "No resume content provided"}), 400
    
    llm, _ = get_ai_components()
    if not llm:
        return jsonify({"error": "LLM not initialized"}), 500
    
    result = generate_resume_feedback(resume_text, target_role, llm)
    return jsonify({"result": as_markdown(result)})

@api_bp.route('/jobs', methods=['POST'])
def find_jobs():
    data = request.json
    role = data.get('role')
    location = data.get('location', 'India')
    
    logger.info(f"API Request: find_jobs for role='{role}' in location='{location}'")
    
    if not role:
        logger.warning("find_jobs: Role is missing")
        return jsonify({"error": "Role is required"}), 400

    try:
        jobs = search_jobs(role, location, Config.SERPAPI_KEY)
        logger.info(f"find_jobs: Found {len(jobs)} jobs for '{role}'")
        return jsonify(jobs)
    except Exception as e:
        logger.error(f"find_jobs Error: {e}")
        return jsonify({"error": str(e)}), 500

