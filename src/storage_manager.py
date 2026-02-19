import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.config import Config
from src.job_processor import Job
from typing import List, Set

class StorageManager:
    def __init__(self):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            Config.GOOGLE_SHEETS_CREDENTIALS_FILE, self.scope
        )
        self.client = gspread.authorize(self.creds)
        
        try:
            self.sheet = self.client.open(Config.SPREADSHEET_NAME).sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            # If not found, one could create it, but for now we assume it exists or we can't really share it with the user easily without their email.
            # Ideally the user creates a sheet and shares it with the service account email.
            print(f"Spreadsheet '{Config.SPREADSHEET_NAME}' not found. Please create it and share with the service account.")
            raise

    def get_existing_urls(self) -> Set[str]:
        """Returns a set of URLs already in the sheet to avoid duplicates."""
        try:
            # Assuming URL is in column 6 (F) based on our schema below
            # Date, Source, Title, Company, Location, URL, Score, Status, Notes
            urls = self.sheet.col_values(6) 
            return set(urls)
        except Exception as e:
            print(f"Error reading existing URLs: {e}")
            return set()

    def save_jobs(self, jobs: List[Job]) -> List[Job]:
        if not jobs:
            return []

        existing_urls = self.get_existing_urls()
        new_jobs = [job for job in jobs if job.url not in existing_urls]
        
        if not new_jobs:
            print("No new jobs to save.")
            return []

        rows_to_append = []
        for job in new_jobs:
            rows_to_append.append([
                job.date_found,
                job.source,
                job.title,
                job.company,
                job.location,
                job.url,
                job.score,
                job.status,
                job.notes
            ])
            
        try:
            self.sheet.append_rows(rows_to_append)
            print(f"Saved {len(new_jobs)} new jobs.")
            return new_jobs
        except Exception as e:
            print(f"Error saving jobs: {e}")
            return []

    def ensure_headers(self):
        """Checks if headers exist, if not adds them."""
        if not self.sheet.get_all_values():
            headers = ["Date Found", "Source", "Title", "Company", "Location", "URL", "Score", "Status", "Notes"]
            self.sheet.append_row(headers)
