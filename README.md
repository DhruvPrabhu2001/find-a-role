# 🕵️ Job Application Discovery Tool

A local tool to discover job opportunities. It aggregates listings from major job boards (LinkedIn, StepStone, Indeed, etc.) using Google Custom Search, scores them based on your personalized profile, and generates a simple **HTML report** for you to check.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

-   **Legal & Compliant**: Uses **Google Custom Search API** to find jobs without scraping.
-   **Configurable Profile**: Edit `src/profile.yaml` to define your target roles, skills, and locations.
-   **Smart Scoring**: Scores jobs (0-100) based on your skills ("Java", "Spring Boot") and keywords.
-   **Auto-Filtering**: Hides "Senior", "Lead" roles automatically.
-   **Simple Report**: Generates a fast, readable `jobs.html` file on your computer.

---

## 🛠️ Prerequisites

1.  **Python 3.10+**.
2.  A **Google Cloud Account** (Free tier).

---

## ⚙️ Setup Guide (15 Mins)

### Phase 1: Google Cloud Setup
1.  Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project.
2.  Enable **"Custom Search API"**.
3.  Create an **API Key** (Credentials > Create Credentials > API Key). Copy it.

### Phase 2: Search Engine Setup
1.  Go to [Programmable Search Engine](https://programmablesearchengine.google.com/).
2.  Click **Add**.
3.  Name: "Job Search".
4.  **What to search**: Select **"Search specific sites or pages"**.
5.  Add these domains:
    -   `*.linkedin.com/jobs`
    -   `*.indeed.de`
    -   `*.stepstone.de`
    -   `*.naukri.com`
    -   `*.wellfound.com`
6.  Click **Create** and get the **Search Engine ID (CX)**.

### Phase 3: Installation
1.  **Clone Repo**:
    ```bash
    git clone https://github.com/DhruvPrabhu2001/find-a-role.git
    cd find-a-role
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure**:
    -   Copy `.env.example` to `.env`.
    -   Fill in your `GOOGLE_API_KEY` and `GOOGLE_CX`.
4.  **Customize**:
    -   Edit `src/profile.yaml` with your skills and locations.

---

## 🏃 Usage

Run the script:
```bash
python -m src.main
```

It will:
1.  Fetch jobs from Google.
2.  Score them.
3.  Create a file named **`jobs.html`**.
4.  Open `jobs.html` in your browser to see the results!

---

## 🤖 Automate (Optional)
You can set up a cron job on your Mac to run this daily:
```bash
0 9 * * * cd /path/to/find-a-role && /usr/bin/python3 -m src.main
```
