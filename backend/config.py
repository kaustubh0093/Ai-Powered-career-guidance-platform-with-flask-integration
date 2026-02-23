import os
from pathlib import Path
from dotenv import load_dotenv

# Define the base directory (root of the project)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables (try root first, then backend folder)
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / ".env")

class Config:
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    @staticmethod
    def validate():
        if not Config.GOOGLE_API_KEY:
            print("⚠️ WARNING: GEMINI_API_KEY not found in environment or .env")
        if not Config.SERPAPI_KEY:
            print("⚠️ WARNING: SERPAPI_API_KEY not found in environment or .env")

# Load and validate on import
Config.validate()

