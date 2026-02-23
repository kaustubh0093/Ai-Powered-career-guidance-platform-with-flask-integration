# 🎯 AI-Powered Career Guidance Platform

An intelligent career guidance application powered by Google Gemini AI, LangChain, and SerpAPI. This platform provides personalized career insights, market analysis, college recommendations, and resume coaching specifically tailored for the Indian job market.

## ✨ Features

### 🧭 Career Insights & Learning Roadmap
- Comprehensive career analysis for various roles across multiple industries
- Detailed learning roadmaps from beginner to advanced levels
- Career progression paths with salary bands (in INR)
- Required skills, tools, and certifications
- Future outlook and industry trends

### 📊 Live Market Analysis
- Real-time job market trends in India
- Current salary ranges (entry/mid/senior levels in INR)
- Top hiring companies and industry sectors
- Major hiring cities (Bangalore, Mumbai, Delhi, Hyderabad, Pune, etc.)
- In-demand skills and remote work availability
- Web-powered live data search using LangChain Agents

### 🎓 College & University Recommendations
- Personalized recommendations for Indian colleges and universities
- IITs, NITs, IIITs, and other premier institutes
- Degree programs, specializations, and eligibility criteria
- Entrance exam information (JEE, GATE, CAT, etc.)
- Scholarships and financial aid options
- Alternative education paths (online courses, bootcamps, certifications)

### 📝 Resume Coach & Feedback
- AI-powered resume analysis and scoring
- Supports **File Upload** (PDF, DOCX, TXT) and **Text Paste**
- ATS (Applicant Tracking System) optimization tips
- Section-by-section detailed feedback
- Content, format, and structure analysis
- Before/After improvement examples
- Industry-specific tips for the Indian job market

### 💬 Interactive AI Career Assistant
- Context-aware conversational AI powered by LangChain Agents
- Ask questions about careers, skills, colleges, and job market
- Personalized guidance and recommendations
- Access to live web data for current information

## 📂 Project Structure

The project follows a modular structure for better maintainability:

```text
ai-career-guide/
├── app.py              # Main Streamlit application entry point
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API keys)
└── src/                # Source code
    ├── components/     # UI components (Chat interface, etc.)
    ├── services/       # Core business logic (AI services, Agent creation)
    ├── data/           # Static data and constants (Career categories)
    ├── utils/          # Utility functions (Text processing)
    └── config.py       # Configuration and API key management
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API Key
- SerpAPI Key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-career-guide
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

**Note:** Never commit your `.env` file to version control. It's included in `.gitignore` for security.

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### SerpAPI Key
1. Visit [SerpAPI](https://serpapi.com/)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key to your `.env` file

### Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🛠️ Technology Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/) - Interactive web application framework
- **AI Model**: [Google Gemini](https://deepmind.google/technologies/gemini/) (gemini-2.0-flash) - Advanced language model
- **AI Framework**: [LangChain](https://www.langchain.com/) - AI application development framework (using Agents for search)
- **Web Search**: [SerpAPI](https://serpapi.com/) - Real-time web search API
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
- **Document Processing**: [PyPDF2](https://pypi.org/project/PyPDF2/) and [python-docx](https://pypi.org/project/python-docx/) - Resume file parsing

## 🇮🇳 Indian Market Focus

This platform is specifically designed for the Indian context:
- Salary ranges in INR (Indian Rupees)
- Indian colleges, universities, and institutions
- Indian entrance exams (JEE, GATE, CAT, etc.)
- Major hiring cities in India
- Indian job market trends and data
- Cultural considerations for Indian recruiters

## 🔒 Security & Privacy

- API keys are stored securely in environment variables or Streamlit secrets
- Never commit `.env` files to version control
- The `.env` file is included in `.gitignore` by default
- No user data is permanently stored or transmitted beyond API calls

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## 📝 License

This project is open source and available for educational and personal use.

## 🙏 Acknowledgments

- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Built with [LangChain](https://www.langchain.com/)
- Web search powered by [SerpAPI](https://serpapi.com/)
- UI framework by [Streamlit](https://streamlit.io/)

---

**Built with ❤️ for career seekers in India**

*Last Updated: February 2025*
