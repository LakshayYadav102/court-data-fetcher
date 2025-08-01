import requests
from bs4 import BeautifulSoup

def extract_case_details_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_case_detail(label):
        td = soup.find("td", string=lambda text: text and label.lower() in text.lower())
        if td:
            next_td = td.find_next_siblings("td")
            if next_td:
                return next_td[-1].get_text(strip=True)
        return "Not found"

    return {
        "petitioner_name": get_case_detail("Petitioner Name"),
        "respondent_name": get_case_detail("Respondent Name"),
        "filing_date": get_case_detail("Filing Date"),
        "court_name": get_case_detail("Court Name"),
        "next_hearing_date": get_case_detail("Next Date of Hearing"),
        "latest_order_link": get_case_detail("View")  # optional
    }

def fetch_case_details(case_type, case_number, case_year, captcha_text):
    session = requests.Session()

    # Step 1: Load the case status page to initialize session cookies
    session.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index")

    # Step 2: Submit the case search form
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/submitCaseNo"

    payload = {
        "state_cd": "13",                 # Haryana
        "dist_cd": "33",                  # Faridabad
        "court_complex_code": "1003",     # Example court complex
        "case_type": case_type,
        "case_number": case_number,
        "case_year": case_year,
        "captcha_code": captcha_text,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.post(url, data=payload, headers=headers)

    # Save response for debugging
    with open("response.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    parsed = extract_case_details_from_html(response.text)
    return response.text, parsed
