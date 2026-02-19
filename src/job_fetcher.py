from googleapiclient.discovery import build
from src.config import Config
from src.job_processor import JobProcessor, Job
from typing import List
import time

class JobFetcher:
    def __init__(self):
        self.service = build("customsearch", "v1", developerKey=Config.GOOGLE_API_KEY)
        
    def fetch_jobs(self) -> List[Job]:
        all_jobs = []
        
        for query in Config.SEARCH_QUERIES:
            print(f"Executing query: {query}")
            try:
                # Fetch first 2 pages (20 results) per query to verify it works
                for start_index in [1, 11]: 
                    res = self.service.cse().list(
                        q=query,
                        cx=Config.GOOGLE_CX,
                        num=10,
                        start=start_index
                    ).execute()
                    
                    items = res.get('items', [])
                    if not items:
                        break
                        
                    for item in items:
                        job = JobProcessor.process_job(item)
                        if job:
                            all_jobs.append(job)
                            
                    time.sleep(1) # Be nice to the API
                    
            except Exception as e:
                print(f"Error fetching jobs for query '{query}': {e}")
                
        return all_jobs
