# Court-Data Fetcher & Mini-Dashboard

## ✅ Overview
This is a web application that allows users to search Indian court cases by selecting a **Case Type**, **Case Number**, and **Filing Year**, then fetches and displays:
- Parties' Names
- Filing & Next-Hearing Dates
- Most Recent Order/Judgment PDF (Downloadable)

**Court Chosen**: Delhi High Court (https://delhihighcourt.nic.in/)

---

## 🛠️ Features

- Form-based UI (HTML + Flask)
- Web scraping with `requests` and `BeautifulSoup`
- CAPTCHA workaround using manual cookie/session strategy (documented below)
- PDF link fetching and local storage
- SQLite for logging case queries and raw responses
- Error-handling for invalid inputs or network issues

---

## 📦 Tech Stack

- Frontend: HTML, Bootstrap
- Backend: Python, Flask
- DB: SQLite (via `sqlite3` module)
- Web Scraping: `requests`, `BeautifulSoup`
- PDF Downloads: `pdf_utils.py`

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/court-data-fetcher.git
cd court-data-fetcher/backend
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```

---

## 🧩 CAPTCHA Strategy

Delhi High Court uses session-based token authentication instead of visual CAPTCHAs. We bypass this by:

- Initiating a session with headers mimicking a browser
- Maintaining the session across all scraping requests
- Capturing hidden fields like `__VIEWSTATE` and passing them forward

> If CAPTCHA changes in future, you'd need to integrate OCR (like pytesseract) or use browser automation (like Playwright/Selenium).

---


## 📋 Sample Query Inputs

- Case Type: W.P.(C)
- Case Number: 12345
- Filing Year: 2023

---

## 📹 Demo Video

A short demo (≤ 5 mins) showing:
- App startup
- Form input
- Output metadata
- PDF preview/download

> Link: [To be uploaded]

---



## 📄 License

MIT License. Feel free to fork and enhance.
