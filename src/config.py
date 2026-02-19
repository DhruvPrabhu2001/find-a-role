import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_profile():
    try:
        with open("src/profile.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Warning: src/profile.yaml not found.")
        return {}

PROFILE = load_profile()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CX = os.getenv("GOOGLE_CX")
    WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY") # CallMeBot API Key
    WHATSAPP_PHONE_NUMBER = os.getenv("WHATSAPP_PHONE_NUMBER") # With Country Code
    
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_FILE = "credentials.json"
    SPREADSHEET_NAME = "Job Application Tracker"
    
    # --- Dynamic Configuration from YAML ---
    
    # Search Configuration
    _sites = " OR ".join(PROFILE.get("search_sites", []))
    _roles = " OR ".join([f'"{r}"' for r in PROFILE.get("target_roles", [])])
    _experience = " OR ".join([f'"{e}"' for e in PROFILE.get("experience_levels", [])])
    _negatives = " ".join([f'-intitle:"{n}"' for n in PROFILE.get("avoid_roles", [])])
    
    # Create queries per major region found in locations
    SEARCH_QUERIES = []
    _locations = PROFILE.get("locations", {})
    
    # Heuristic: only use "Germany", "India", "Remote" or explicitly listed countries for the query location: filter
    # Cities are used for scoring, but for search queries "location:Berlin" works too.
    # Let's just iterate over all location keys with high weight? No, let's Stick to broader regions if possible.
    # For now, we will create a query for each item in 'locations' to be thorough, 
    # OR better: (location:Berlin OR location:Munich OR location:Germany)
    
    _loc_filter = " OR ".join([f'location:"{loc}"' for loc in _locations.keys()])
    
    # Construct single powerful query? Google limits to 32 words often.
    # Better to split. 
    # Let's split by "Germany" VS "India" context if clear, otherwise just 1-2 generic queries.
    
    # Simple approach: Create one query with big OR for locations
    if _loc_filter:
        SEARCH_QUERIES.append(f'({_sites}) ({_roles}) ({_experience}) ({_loc_filter}) {_negatives}')
    else:
        SEARCH_QUERIES.append(f'({_sites}) ({_roles}) ({_experience}) {_negatives}')

    # Filtering & Scoring
    KEYWORDS_WEIGHTS = PROFILE.get("skills", {})
    
    TITLE_KEYWORDS = {role: 10 for role in PROFILE.get("target_roles", [])}
    for exp in PROFILE.get("experience_levels", []):
         TITLE_KEYWORDS[exp] = 10
    
    NEGATIVE_TITLE_KEYWORDS = PROFILE.get("avoid_roles", [])
    
    LOCATION_WEIGHTS = PROFILE.get("locations", {})
    
    VISA_KEYWORDS = PROFILE.get("visa_keywords", [])
    VISA_SCORE = 20
    
    BASE_SCORE = 50
