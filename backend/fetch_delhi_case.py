from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

def fetch_delhi_case_details(case_type, case_number, case_year):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        # Select case type
        wait.until(EC.presence_of_element_located((By.ID, "case_type")))
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

        # Enter case number
        driver.find_element(By.ID, "case_number").send_keys(case_number)

        # Select case year
        Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(case_year)

        # Wait for CAPTCHA text and input
        wait.until(EC.presence_of_element_located((By.ID, "captcha-code")))
        wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))

        # Read CAPTCHA from span
        captcha_text = driver.find_element(By.ID, "captcha-code").text.strip()
        driver.find_element(By.ID, "captchaInput").send_keys(captcha_text)

        # ✅ Fix: Use XPATH to find the Submit button since it has no ID
        submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
        submit_button.click()

        # Optional: wait for table to appear or fallback to sleep
        time.sleep(5)

        # Save result HTML
        html = driver.page_source
        with open("response.html", "w", encoding="utf-8") as f:
            f.write(html)

        return {
            "status": "submitted",
            "captcha_used": captcha_text,
            "html_saved": True
        }

    except Exception as e:
        driver.save_screenshot("fatal_error.png")
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

    finally:
        driver.quit()
