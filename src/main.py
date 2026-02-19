from src.job_fetcher import JobFetcher
from src.report_generator import ReportGenerator
import sys

def main():
    print("Starting Job Application Tracking System...")
    
    try:
        # Initialize components
        fetcher = JobFetcher()
        reporter = ReportGenerator("jobs.html")
        
        # 1. Fetch Jobs
        print("Fetching jobs...")
        jobs = fetcher.fetch_jobs()
        print(f"Fetched {len(jobs)} jobs.")
        
        # 2. Generate Report (One file to check)
        print("Generating report...")
        reporter.generate_report(jobs)
        
        print("Job scan completed successfully. Open 'jobs.html' to see results.")
        
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
