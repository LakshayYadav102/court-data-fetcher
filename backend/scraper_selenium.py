from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import traceback

def fetch_case_details_selenium(state, district, court_complex, case_type, case_number, case_year):
    # Clean inputs
    state = state.strip().title()
    district = district.strip().title()
    court_complex = court_complex.strip()
    case_type = case_type.strip()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index")

        # Select State
        wait.until(EC.presence_of_element_located((By.ID, "sess_state_code")))
        Select(driver.find_element(By.ID, "sess_state_code")).select_by_visible_text(state)
        time.sleep(1)  # Wait for districts to populate

        # Select District
        Select(driver.find_element(By.ID, "sess_dist_code")).select_by_visible_text(district)
        time.sleep(1.5)  # Wait for court complexes to populate

        # Select Court Complex
        complex_dropdown = Select(driver.find_element(By.ID, "court_complex_code"))
        available_complexes = [opt.text.strip() for opt in complex_dropdown.options]
        if court_complex not in available_complexes:
            driver.save_screenshot("error_court_complex.png")
            return {
                "error": f"Court Complex '{court_complex}' not found.",
                "available": available_complexes
            }
        complex_dropdown.select_by_visible_text(court_complex)
        time.sleep(1)

        # ✅ Switch to "Case Number" tab
        case_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#case_number']")))
        case_tab.click()
        time.sleep(1)

        # ✅ Select case type
        wait.until(lambda d: len(Select(d.find_element(By.ID, "case_type")).options) > 1)
        case_dropdown = Select(driver.find_element(By.ID, "case_type"))
        available_case_types = [opt.text.strip() for opt in case_dropdown.options]
        if case_type not in available_case_types:
            driver.save_screenshot("error_case_type.png")
            return {
                "error": f"Case Type '{case_type}' not found.",
                "available": available_case_types
            }
        case_dropdown.select_by_visible_text(case_type)

        # ✅ Fill case number and year
        driver.find_element(By.ID, "case_no").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(case_year)

        # ✅ Select Pending radio
        try:
            driver.find_element(By.XPATH, "//input[@name='case_status' and @value='P']").click()
        except:
            driver.save_screenshot("error_case_status_radio.png")
            return {"error": "Could not select case status radio button"}

        time.sleep(1)

        # ✅ CAPTCHA Screenshot
        captcha_img = driver.find_element(By.ID, "captcha_image").screenshot_as_png
        with open("captcha.png", "wb") as f:
            f.write(captcha_img)

        print("⚠️  Check 'captcha.png' and enter CAPTCHA manually:")
        captcha = input("Enter CAPTCHA: ")

        driver.find_element(By.ID, "captcha").send_keys(captcha)
        driver.find_element(By.ID, "submit").click()

        time.sleep(3)

        html = driver.page_source
        with open("response.html", "w", encoding="utf-8") as f:
            f.write(html)

        return {"status": "Success", "html_saved": True}

    except Exception as e:
        driver.save_screenshot("fatal_error.png")
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

    finally:
        driver.quit()
