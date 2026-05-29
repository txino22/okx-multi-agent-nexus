import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Google Cloud / Vertex AI Runtime Configuration
USE_VERTEX_AI = os.environ.get("USE_VERTEX_AI", "true").lower() == "true"
GCP_PROJECT = os.environ.get("GCP_PROJECT", "")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

# Model Selection: default to gemini-2.5-flash for Vertex AI compatibility
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

INTERFACE_MODEL = os.environ.get("INTERFACE_MODEL", "gemini-2.5-flash")
ANALYST_MODEL = os.environ.get("ANALYST_MODEL", "gemini-2.5-flash")
STRATEGIST_MODEL = os.environ.get("STRATEGIST_MODEL", "gemini-2.5-pro")

# Gemini API Key (Fallback if USE_VERTEX_AI=false)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# OKX API Authentication
OKX_API_KEY = os.environ.get("OKX_API_KEY", "")
OKX_SECRET_KEY = os.environ.get("OKX_SECRET_KEY", "")
OKX_PASSPHRASE = os.environ.get("OKX_PASSPHRASE", "")

# Trading environment mode: 'demo' (default) or 'live'
OKX_MODE = os.environ.get("OKX_MODE", "demo").lower()

def validate_config():
    """Prints warning logs if configuration seems incomplete or placeholder-based."""
    warnings = []
    
    if USE_VERTEX_AI:
        if not GCP_PROJECT or GCP_PROJECT == "mock-gcp-project-id":
            warnings.append("GCP_PROJECT is missing or set to placeholder.")
        if not GCP_LOCATION:
            warnings.append("GCP_LOCATION is missing (defaulting to us-central1).")
    else:
        if not GEMINI_API_KEY or GEMINI_API_KEY == "mock-gemini-api-key":
            warnings.append("GEMINI_API_KEY is missing or set to placeholder.")
            
    if not OKX_API_KEY or OKX_API_KEY == "mock-okx-api-key":
        warnings.append("OKX_API_KEY is missing or set to placeholder.")
    if not OKX_SECRET_KEY or OKX_SECRET_KEY == "mock-okx-api-secret":
        warnings.append("OKX_SECRET_KEY is missing or set to placeholder.")
    if not OKX_PASSPHRASE or OKX_PASSPHRASE == "mock-okx-passphrase":
        warnings.append("OKX_PASSPHRASE is missing or set to placeholder.")
        
    if warnings:
        print("\n\033[93m[CONFIG WARNINGS]\033[0m The following environment variables are not fully configured:")
        for w in warnings:
            print(f" - {w}")
        print("Please configure them in your .env file for correct cloud runtime and OKX trading.\n")
    else:
        print("\n\033[92m[CONFIG SUCCESS]\033[0m Configuration successfully validated for " + 
              ("Vertex AI" if USE_VERTEX_AI else "Gemini API") + 
              f" runtime and OKX '{OKX_MODE}' trading.\n")
