import requests
from src.config import Config
from src.job_processor import Job
from typing import List
import urllib.parse

class Notifier:
    def __init__(self):
        self.api_key = Config.WHATSAPP_API_KEY
        self.phone_number = Config.WHATSAPP_PHONE_NUMBER
        
    def send_daily_summary(self, jobs: List[Job]):
        if not jobs:
            print("No new jobs to notify about.")
            return

        # Sort by score descending
        sorted_jobs = sorted(jobs, key=lambda x: x.score, reverse=True)
        top_jobs = sorted_jobs[:10] # Top 10 only (WhatsApp msg length limits)
        
        # WhatsApp supports simpler formatting: *bold*, _italic_, ~strikethrough~
        message = f"🚀 *Daily Job Summary* ({len(jobs)} new)\n\n"
        
        for job in top_jobs:
            # Create a clean message
            # Note: WhatsApp links preview automatically if they are the first link, 
            # but we have multiple. Just listing them is fine.
            icon = "🔥" if job.score > 70 else "💼"
            message += f"{icon} *{job.title}* ({job.score})\n"
            message += f"🏢 {job.company} | 📍 {job.location}\n"
            message += f"🔗 {job.url}\n\n"
            
        if len(jobs) > 10:
            message += f"_...and {len(jobs) - 10} more in the sheet._"

        self._send_message(message)

    def _send_message(self, text: str):
        # CallMeBot API: https://api.callmebot.com/whatsapp.php?phone=[phone]&text=[text]&apikey=[apikey]
        encoded_text = urllib.parse.quote(text)
        url = f"https://api.callmebot.com/whatsapp.php?phone={self.phone_number}&text={encoded_text}&apikey={self.api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("WhatsApp notification sent successfully.")
            else:
                print(f"Failed to send WhatsApp notification. Status: {response.status_code}")
        except Exception as e:
            print(f"Error sending WhatsApp notification: {e}")
