import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CX = os.getenv("GOOGLE_CX")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_FILE = "credentials.json"
    SPREADSHEET_NAME = "Job Application Tracker"
    
    # Search Configuration
    # Targeted search queries for Google Custom Search
    SEARCH_QUERIES = [
        # Germany - Java/Backend
        '(site:linkedin.com/jobs/view OR site:stepstone.de OR site:indeed.de) ("Java" AND "Spring Boot") ("Junior" OR "Associate" OR "0-2 years") location:Germany -intitle:Senior -intitle:Lead',
        # India - Java/Backend
        '(site:linkedin.com/jobs/view OR site:naukri.com) ("Java" AND "Spring Boot") ("Junior" OR "Associate" OR "0-2 years") location:India -intitle:Senior -intitle:Lead'
    ]
    
    # Filtering & Scoring
    KEYWORDS_WEIGHTS = {
        "Spring Boot": 10,
        "Java": 10,
        "Rest API": 5,
        "Hibernate": 5,
        "Microservices": 5,
        "AWS": 5
    }
    
    TITLE_KEYWORDS = {
        "Junior": 20,
        "Associate": 20,
        "Trainee": 10,
        "Werkstudent": 5, # Working student in German
        "Intern": 5
    }
    
    NEGATIVE_TITLE_KEYWORDS = [
        "Senior", "Lead", "Principal", "Architect", "Manager", "Head of"
    ]
    
    LOCATION_WEIGHTS = {
        "Berlin": 10,
        "Munich": 10,
        "Hamburg": 10,
        "Frankfurt": 10,
        "Remote": 15
    }
    
    VISA_KEYWORDS = ["Visa sponsorship", "Relocation", "Visa support"]
    VISA_SCORE = 20
    
    BASE_SCORE = 50
