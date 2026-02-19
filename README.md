# Job Application Tracking System

A semi-automated system to track and filter job applications for a Junior Backend Engineer profile targeting Germany and India.
It aggregates jobs using Google Custom Search, filters them based on keywords and location, scores them, and saves them to a Google Sheet. It also sends daily summaries via Telegram.

## 🚀 Features
- **Smart Search**: Uses Google Custom Search to legally find jobs on LinkedIn, StepStone, Indeed, etc.
- **Auto-Filtering**: Ignores "Senior", "Lead" roles. Prioritizes "Junior", "Associate".
- **Scoring System**: Scores jobs based on keywords (Java, Spring Boot), location, and visa sponsorship.
- **Duplicates Removal**: Checks against existing URLs in Google Sheets.
- **Telegram Notifications**: specific daily summary of top jobs.
- **Results in Google Sheets**: Keeps a structured database of leads.

## 🛠️ Prerequisites
- Python 3.10+
- A Google Cloud Project with "Custom Search API" enabled.
- A Telegram Bot.

## ⚙️ Setup (Estimated Time: ~30 mins)

### 1. Google Cloud Setup
1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a project and enable **Custom Search API** and **Google Sheets API**.
3.  Create an API Key for Custom Search.
4.  Create a Service Account for Sheets, download the JSON key, rename it to `credentials.json`, and place it in the project root.
5.  Create a [Programmable Search Engine (CSE)](https://programmablesearchengine.google.com/).
    -   Select "Search the entire web" but strictly we filter in search queries using `site:linkedin.com` etc.
    -   Or add specific sites: `linkedin.com/jobs`, `stepstone.de`, `indeed.de`, `naukri.com`.
    -   Get the **Search Engine ID (CX)**.

### 2. Google Sheets
1.  Create a new Google Sheet.
2.  Share it with the `client_email` found in your `credentials.json`.
3.  Note the Sheet Name (default: "Job Application Tracker").

### 3. Telegram Bot
1.  Chat with `@BotFather` on Telegram to create a new bot.
2.  Get the **Bot Token**.
3.  Start a chat with your bot and get your **Chat ID** (use `@userinfobot` or look at API updates).

### 4. Local Installation
```bash
# Clone repository
git clone <your-repo>
cd find-a-role

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# Edit .env and add your API Keys
```

## 🏃 Usage

### Run Manually
```bash
python -m src.main
```

### GitHub Actions (Automated)
1.  Push code to GitHub.
2.  Add the following **Repository Secrets**:
    -   `GOOGLE_API_KEY`
    -   `GOOGLE_CX`
    -   `TELEGRAM_BOT_TOKEN`
    -   `TELEGRAM_CHAT_ID`
    -   `GOOGLE_CREDENTIALS_JSON` (Paste the content of credentials.json)
3.  The workflow `Daily Job Scan` will run every day at 08:00 UTC.

## 🧪 Testing
Run unit tests to verify scoring logic:
```bash
python -m unittest tests/test_logic.py
```
