# 🕵️ Job Application Tracking System

A smart, semi-automated tool to track and discover job opportunities. It aggregates listings from known job boards (LinkedIn, StepStone, Indeed, etc.) using Google Custom Search, scores them based on your personalized profile, and organizes them in Google Sheets. You get a daily summary via **WhatsApp**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

-   **Legal & Compliant**: Uses **Google Custom Search API** to find jobs without scraping or violating Terms of Service.
-   **Configurable Profile**: meaningful configuration via `src/profile.yaml`. Define your target roles, skills, and locations easily.
-   **Smart Scoring**: Scores jobs based on your skills ("Java", "Spring Boot"), experience level, and visa sponsorship.
-   **Auto-Filtering**: Filters out irrelevant roles (e.g., "Senior", "Lead", "Principal") to keep your feed clean.
-   **Data Storage**: Saves all findings to **Google Sheets**, handling deduplication automatically.
-   **Daily Notifications**: Sends a concise summary of the top-scored jobs to your **WhatsApp**.
-   **Automation Ready**: Includes a **GitHub Actions** workflow to run daily at 08:00 UTC for free.

---

## 🛠️ Prerequisites

Before you start, ensure you have:
1.  **Python 3.10+** installed.
2.  A **Google Cloud Account** (Free tier is sufficient).
3.  A **WhatsApp Account**.

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
    -   Select **"Search specific sites or pages"**.
    -   Add the following domains manually:
        -   `*.linkedin.com/jobs`
        -   `*.indeed.de`
        -   `*.stepstone.de`
        -   `*.naukri.com`
        -   `*.wellfound.com`
5.  Click **Create**.
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

### Phase 4: WhatsApp Setup (CallMeBot)
We use **CallMeBot**, a free API for personal WhatsApp notifications.
1.  Add the phone number **`+34 644 10 55 84`** to your Phone Contacts. (Name it "CallMeBot").
2.  Send this message to the new contact: `I allow callmebot to send me messages`
3.  Wait until you receive the message "API Activated for your phone number. Your APIKEY is 123456".
4.  Note your **API Key** and **Phone Number** (with country code, e.g., `+49...`).

### Phase 5: Local Installation & Configuration
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/DhruvPrabhu2001/find-a-role.git
    cd find-a-role
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    -   Copy the example file:
        ```bash
        cp .env.example .env
        ```
    -   Open `.env` and fill in your keys:
        ```ini
        GOOGLE_API_KEY=...
        GOOGLE_CX=...
        WHATSAPP_API_KEY=...       # From CallMeBot
        WHATSAPP_PHONE_NUMBER=...  # e.g. +49123456789 (your number)
        ```

4.  **Customize Your Profile**:
    -   Open `src/profile.yaml`.
    -   Update **target_roles**, **skills**, and **locations**.

---

## 🏃 Usage
```bash
python -m src.main
```

##  Automation (GitHub Actions)
1.  Push code to GitHub.
2.  Add **Repository Secrets**:
    -   `GOOGLE_API_KEY`, `GOOGLE_CX`
    -   `WHATSAPP_API_KEY`, `WHATSAPP_PHONE_NUMBER`
    -   `GOOGLE_CREDENTIALS_JSON`
3.  Runs daily at **08:00 UTC**.

---

Made with ❤️ by Antigravity
