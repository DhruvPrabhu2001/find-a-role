from src.job_fetcher import JobFetcher
from src.storage_manager import StorageManager
from src.notifier import Notifier
import sys

def main():
    print("Starting Job Application Tracking System...")
    
    try:
        # Initialize components
        fetcher = JobFetcher()
        storage = StorageManager()
        notifier = Notifier()
        
        # Ensure sheet headers exist
        storage.ensure_headers()
        
        # 1. Fetch Jobs
        print("Fetching jobs...")
        jobs = fetcher.fetch_jobs()
        print(f"Fetched {len(jobs)} jobs.")
        
        # 2. Save to Sheet & Deduplicate
        print("Saving to Google Sheets...")
        new_jobs = storage.save_jobs(jobs)
        
        # 3. Notify if new jobs found
        if new_jobs:
            print(f"Sending notification for {len(new_jobs)} new jobs...")
            notifier.send_daily_summary(new_jobs)
        else:
            print("No new jobs to notify.")
            
        print("Job scan completed successfully.")
        
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
