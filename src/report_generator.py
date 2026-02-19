from src.job_processor import Job
from typing import List
import os

class ReportGenerator:
    def __init__(self, output_file: str = "jobs.html"):
        self.output_file = output_file
        
    def generate_report(self, jobs: List[Job]):
        if not jobs:
            print("No jobs to report.")
            return

        sorted_jobs = sorted(jobs, key=lambda x: x.score, reverse=True)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Job Board</title>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .job-card {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; }}
                .high-score {{ border-left: 5px solid #2ecc71; background-color: #f9fdfa; }}
                .medium-score {{ border-left: 5px solid #f1c40f; }}
                .title {{ font-size: 1.2em; font-weight: bold; }}
                .meta {{ color: #666; font-size: 0.9em; margin-bottom: 5px; }}
                .score {{ float: right; font-weight: bold; background: #eee; padding: 2px 6px; border-radius: 4px; }}
                a {{ text-decoration: none; color: #3498db; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>Found {len(jobs)} Jobs</h1>
            <p>Generated on: {jobs[0].date_found}</p>
        """
        
        for job in sorted_jobs:
            score_class = "high-score" if job.score >= 70 else "medium-score"
            html_content += f"""
            <div class="job-card {score_class}">
                <div class="score">{job.score}</div>
                <div class="title"><a href="{job.url}" target="_blank">{job.title}</a></div>
                <div class="meta">{job.company} | {job.location} | {job.source}</div>
                <div class="snippet">{job.description_snippet}</div>
            </div>
            """
            
        html_content += """
        </body>
        </html>
        """
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Report generated successfully: {os.path.abspath(self.output_file)}")
