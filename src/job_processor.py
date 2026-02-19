from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from src.config import Config

@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str
    source: str
    date_found: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    score: int = 0
    status: str = "New"
    notes: str = ""
    description_snippet: str = ""

class JobProcessor:
    @staticmethod
    def calculate_score(job: Job) -> int:
        score = Config.BASE_SCORE
        
        # Title Scoring
        for keyword, weight in Config.TITLE_KEYWORDS.items():
            if keyword.lower() in job.title.lower():
                score += weight
                
        # Negative Title Scoring (Filter out senior roles)
        for keyword in Config.NEGATIVE_TITLE_KEYWORDS:
            if keyword.lower() in job.title.lower():
                score -= 50 # Heavy penalty
                
        # Location Scoring
        for location, weight in Config.LOCATION_WEIGHTS.items():
            if location.lower() in job.location.lower():
                score += weight
                
        # Keyword Scoring (in title or snippet)
        full_text = (job.title + " " + job.description_snippet).lower()
        for keyword, weight in Config.KEYWORDS_WEIGHTS.items():
            if keyword.lower() in full_text:
                score += weight
                
        # Visa Scoring
        for keyword in Config.VISA_KEYWORDS:
            if keyword.lower() in full_text:
                score += Config.VISA_SCORE
                break # count once
                
        return score

    @staticmethod
    def process_job(item: dict) -> Optional[Job]:
        """
        Converts a Google Custom Search Result item into a Job object.
        """
        title_full = item.get('title', '')
        link = item.get('link', '')
        snippet = item.get('snippet', '')
        
        # Simple parsing logic (heuristics)
        # Often titles are "Role at Company" or "Company - Role"
        # We'll improve this with regex if needed, but for now exact extraction is hard without specific scraping.
        # We will use the full title string.
        
        # Attempt to split Title and Company
        # Common patterns: "Job Title - Company - Location" or "Job Title at Company"
        title = title_full
        company = "Unknown"
        location = "Unknown"
        
        if " - " in title_full:
            parts = title_full.split(" - ")
            title = parts[0]
            if len(parts) > 1:
                company = parts[1]
        elif " at " in title_full:
            parts = title_full.split(" at ")
            title = parts[0]
            if len(parts) > 1:
                # sometimes "at Company"
                company = parts[1]

        # infer location from snippet or title if possible, else default to Unknown
        # We can check if any known location is in the string
        for loc in Config.LOCATION_WEIGHTS.keys():
            if loc.lower() in (title_full + snippet).lower():
                location = loc
                break
        
        # Identify source
        source = "Web"
        if "linkedin.com" in link:
            source = "LinkedIn"
        elif "indeed" in link:
            source = "Indeed"
        elif "stepstone" in link:
            source = "StepStone"
        elif "naukri" in link:
            source = "Naukri"
            
        job = Job(
            title=title,
            company=company,
            location=location,
            url=link,
            source=source,
            description_snippet=snippet
        )
        
        job.score = JobProcessor.calculate_score(job)
        
        # Filter out low scores or negative keywords
        if job.score < 30: # Threshold
            return None
            
        return job
