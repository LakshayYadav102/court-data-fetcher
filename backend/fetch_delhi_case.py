from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
import os
from bs4 import BeautifulSoup

from parser import parse_case_details
from database import log_query
from pdf_utils import save_case_pdf

def fetch_delhi_case_details(case_type, case_number, case_year):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        # Select case type
        wait.until(EC.presence_of_element_located((By.ID, "case_type")))
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

        # Enter case number and year
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(case_year)

        # Handle CAPTCHA
        wait.until(EC.presence_of_element_located((By.ID, "captcha-code")))
        wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
        captcha_text = driver.find_element(By.ID, "captcha-code").text.strip()
        driver.find_element(By.ID, "captchaInput").send_keys(captcha_text)

        # Click submit
        submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
        submit_button.click()

        # Wait for page load
        time.sleep(5)

        html = driver.page_source

        # Log and parse
        log_query(case_type, case_number, case_year, html)
        parsed_result = parse_case_details(html)

        # Fetch the latest order PDF link if pdf_link exists
        latest_order_pdf = "Not Available"
        debug_info = []
        if parsed_result.get("pdf_link"):
            debug_info.append(f"Navigating to pdf_link: {parsed_result['pdf_link']}")
            driver.get(parsed_result["pdf_link"])
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
            time.sleep(3)  # Allow dynamic content to load
            page_html = driver.page_source
            # Save debug HTML
            debug_path = os.path.join("debug", f"case_details_{case_type}_{case_number}_{case_year}.html")
            os.makedirs(os.path.dirname(debug_path), exist_ok=True)
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(page_html)
            soup = BeautifulSoup(page_html, "html.parser")
            # Target the first row, second column (Order Link)
            order_row = soup.select_one("table tbody tr")
            if order_row:
                debug_info.append("Found first table row")
                cells = order_row.find_all("td")
                if len(cells) >= 2:
                    debug_info.append(f"Found {len(cells)} cells in first row")
                    order_link = cells[1].find("a", href=True)
                    if order_link and order_link["href"]:
                        order_url = order_link["href"]
                        debug_info.append(f"Order link found: {order_url}")
                        if order_url.startswith("http") and "showlogo" in order_url and ".pdf" in order_url:
                            latest_order_pdf = order_url
                        elif not order_url.startswith("http"):
                            latest_order_pdf = "https://delhihighcourt.nic.in" + order_url
                            debug_info.append(f"Converted to absolute URL: {latest_order_pdf}")
                    else:
                        debug_info.append("No order link found in second column")
                else:
                    debug_info.append("Insufficient cells in first row")
            else:
                debug_info.append("No table rows found")
            # Save debug info
            with open(debug_path, "a", encoding="utf-8") as f:
                f.write("\n\nDebug Info:\n" + "\n".join(debug_info))

        # Save parsed result to PDF
        output_path = os.path.join("pdfs", f"{case_type}_{case_number}_{case_year}.pdf")
        save_case_pdf(parsed_result, output_path)

        return {
            "captcha_used": captcha_text,
            "parsed_result": {
                **parsed_result,
                "latest_order_pdf": latest_order_pdf
            },
            "pdf_path": output_path
        }

    except Exception as e:
        driver.save_screenshot("fatal_error.png")
        debug_path = os.path.join("debug", f"case_details_{case_type}_{case_number}_{case_year}.html")
        with open(debug_path, "a", encoding="utf-8") as f:
            f.write(f"\n\nError: {str(e)}\nTrace: {traceback.format_exc()}")
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

    finally:
        driver.quit()