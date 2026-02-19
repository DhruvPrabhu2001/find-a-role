import requests
from src.config import Config
from src.job_processor import Job
from typing import List

class Notifier:
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        
    def send_daily_summary(self, jobs: List[Job]):
        if not jobs:
            print("No new jobs to notify about.")
            return

        # Sort by score descending
        sorted_jobs = sorted(jobs, key=lambda x: x.score, reverse=True)
        top_jobs = sorted_jobs[:10] # Top 10 only to avoid spam
        
        message = f"🚀 **Daily Job Summary** ({len(jobs)} new)\n\n"
        
        for job in top_jobs:
            icon = "🔥" if job.score > 70 else "💼"
            message += f"{icon} [{job.score}] <a href='{job.url}'>{job.title}</a>\n"
            message += f"🏢 {job.company} | 📍 {job.location}\n\n"
            
        if len(jobs) > 10:
            message += f"<i>...and {len(jobs) - 10} more in the sheet.</i>"

        self._send_message(message)

    def _send_message(self, text: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Notification sent successfully.")
        except Exception as e:
            print(f"Error sending notification: {e}")
