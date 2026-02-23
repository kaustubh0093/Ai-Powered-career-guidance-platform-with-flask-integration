import os
import streamlit as st
from typing import Dict, Optional

def load_api_keys() -> Dict[str, Optional[str]]:
    google_api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    serpapi_key = os.getenv("SERPAPI_API_KEY") or st.secrets.get("SERPAPI_API_KEY", "")
    return {"google_api_key": google_api_key, "serpapi_key": serpapi_key}
