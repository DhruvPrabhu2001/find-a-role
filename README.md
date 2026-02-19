# 🕵️ Job Application Tracking System

A smart, semi-automated tool to track and discover job opportunities. It aggregates listings from major job boards (LinkedIn, StepStone, Indeed, etc.) using Google Custom Search, scores them based on your personalized profile, and organizes them in Google Sheets. You get a daily summary via Telegram.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

-   **Legal & Compliant**: Uses **Google Custom Search API** to find jobs without scraping or violating Terms of Service.
-   **Configurable Profile**: meaningful configuration via `src/profile.yaml`. Define your target roles, skills, and locations easily.
-   **Smart Scoring**: Scores jobs based on your skills ("Java", "Spring Boot"), experience level, and visa sponsorship.
-   **Auto-Filtering**: Filters out irrelevant roles (e.g., "Senior", "Lead", "Principal") to keep your feed clean.
-   **Data Storage**: Saves all findings to **Google Sheets**, handling deduplication automatically.
-   **Daily Notifications**: Sends a concise summary of the top-scored jobs to your **Telegram**.
-   **Automation Ready**: Includes a **GitHub Actions** workflow to run daily at 08:00 UTC for free.

---

## 🛠️ Prerequisites

Before you start, ensure you have:
1.  **Python 3.10+** installed.
2.  A **Google Cloud Account** (Free tier is sufficient).
3.  A **Telegram Account**.

---

## ⚙️ Setup Guide (Start Here)

Follow these steps to get the system running in about 20-30 minutes.

### Phase 1: Google Cloud Setup (Search API)
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project (e.g., `job-tracker`).
3.  **Enable APIs**:
    -   Go to **APIs & Services > Library**.
    -   Search for and enable **"Custom Search API"**.
    -   Search for and enable **"Google Sheets API"**.
    -   Search for and enable **"Google Drive API"**.
4.  **Create API Key**:
    -   Go to **APIs & Services > Credentials**.
    -   Click **Create Credentials > API Key**.
    -   Copy this key. (You will need it as `GOOGLE_API_KEY`).

### Phase 2: Google Custom Search Engine (CSE)
1.  Go to [Programmable Search Engine](https://programmablesearchengine.google.com/).
2.  Click **Add**.
3.  **Name**: "Job Search".
4.  **What to search**:
    -   Google changed the UI recently. You *must* add at least one specific site to create the engine initially.
    -   Enter: `training.google.com` (or any dummy site).
    -   Click **Create**.
5.  **Enable "Search the entire web"**:
    -   Click on the search engine you just created to open the **Control Panel**.
    -   In the **Overview** (or "Basics") tab, look for **"Search the entire web"**.
    -   **Toggle it ON**.
    -   *(Optional)* You can now delete the dummy site (`training.google.com`) from the list below if you wish.
6.  Copy the **Search Engine ID (CX)**. (You will need it as `GOOGLE_CX`).

### Phase 3: Google Sheets & Service Account
1.  **Create Service Account**:
    -   Back in Google Cloud Console > **Credentials**.
    -   Click **Create Credentials > Service Account**.
    -   Name it (e.g., `job-bot`). Click **Done**.
    -   Click on the newly created service account email.
    -   Go to the **Keys** tab > **Add Key** > **Create new key** > **JSON**.
    -   A file will download. **Rename it** to `credentials.json` and place it in the project root folder.
2.  **Create Spreadsheet**:
    -   Go to [Google Sheets](https://docs.google.com/spreadsheets).
    -   Create a new blank sheet. Name it **"Job Application Tracker"**.
    -   **Important**: Click **Share** (top right) and paste the **client_email** found inside your `credentials.json` file. Give it **Editor** access.

### Phase 4: Telegram Bot Setup
1.  Open Telegram and search for **@BotFather**.
2.  Send the command `/newbot`.
3.  Follow instructions to name your bot.
4.  Copy the **HTTP API Token**. (You will need it as `TELEGRAM_BOT_TOKEN`).
5.  **Get Chat ID**:
    -   Start a chat with your new bot and send "Hello".
    -   Visit this URL in your browser: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
    -   Look for `"chat":{"id":123456789...}`. That number is your `TELEGRAM_CHAT_ID`.

### Phase 5: Local Installation & Configuration
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/DhruvPrabhu2001/find-a-role.git
    cd find-a-role
    ```

2.  **Install Dependencies**:
    ```bash
    # (Optional) Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install requirements
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    -   Copy the example file:
        ```bash
        cp .env.example .env
        ```
    -   Open `.env` and fill in the keys you generated above:
        ```ini
        GOOGLE_API_KEY=your_api_key_here
        GOOGLE_CX=your_cx_id_here
        TELEGRAM_BOT_TOKEN=your_bot_token_here
        TELEGRAM_CHAT_ID=your_chat_id_here
        ```

4.  **Customize Your Profile**:
    -   Open `src/profile.yaml`.
    -   Update **target_roles**, **skills**, and **locations** to match your preferences.
    -   *Tip: The system uses these to generate search queries and score jobs.*

---

## 🏃 Usage

### Run Manually
To perform a one-time scan:
```bash
python -m src.main
```
You should see output indicating:
1.  Jobs being fetched.
2.  Jobs being saved to Google Sheets.
3.  A notification sent to Telegram.

### 🧪 Run Tests
To verify the scoring logic works as expected:
```bash
python -m unittest tests/test_logic.py
```

---

## 🤖 Automation (GitHub Actions)

To have this run automatically every day:

1.  Push your code to your GitHub repository.
2.  Go to **Settings > Secrets and variables > Actions**.
3.  Add the following **Repository Secrets**:
    -   `GOOGLE_API_KEY`
    -   `GOOGLE_CX`
    -   `TELEGRAM_BOT_TOKEN`
    -   `TELEGRAM_CHAT_ID`
    -   `GOOGLE_CREDENTIALS_JSON` -> **Paste the entire content** of your `credentials.json` file here.
4.  The workflow is configured in `.github/workflows/daily_job_scan.yml` to run daily at **08:00 UTC**.

---

## ❓ Troubleshooting

-   **"Spreadsheet not found"**: Ensure the generic `SPREADSHEET_NAME` in `src/config.py` (which defaults to "Job Application Tracker") matches your actual sheet name exactly, OR rename your sheet to match.
-   **"Quota Exceeded"**: The Google Custom Search API specific free tier allows 100 queries/day. If you have many combinations in `profile.yaml`, you might hit this. Reduce the number of targeted locations or sites if needed.
-   **No Telegram Message**: Ensure you have started a conversation with your bot first. Bots cannot initiate conversations with users who haven't messaged them.

---

Made with ❤️ by Antigravity
