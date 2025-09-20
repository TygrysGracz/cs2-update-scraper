from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.counter-strike.net/news/updates")
driver.implicitly_wait(5)

# Valve has the same class name for every update block, so it's easy to scrape them.
updates = driver.find_elements(By.CLASS_NAME, "-EouvmnKRMabN5fJonx-O")

# Checks how many updates were found
print("Found: ", len(updates))
time.sleep(5)

for upd in updates:

    # Date
    try:
        date = upd.find_element(By.CLASS_NAME, "gvPzKyr8etHG1aBrpLeNJ").text
    except:
        date = ""

    # Title
    try:
        title = upd.find_element(By.CLASS_NAME, "_13NfC6a7fAZHtLoSD39KO1").text
    except:
        title = ""

    print(f"\nDate: {date}")
    print(f"Title: {title}")
    print("=" * 50)

    # Content
    content_divs = upd.find_elements(By.CLASS_NAME, "_2s0cUiQc0Xlgvxtq_9CH8J")
    for content in content_divs:

        headers = content.find_elements(By.CLASS_NAME, "_23SXWVQfREeO5DYXHTgcWK")
        for h in headers:
            text = h.text.strip()
            if not text:
                continue
            if text.startswith("[") and text.endswith("]"):
                print(f"[HEADER] {text}")
            else:
                print(f"[PARAGRAPH] {text}")


        uls = content.find_elements(By.CLASS_NAME, "cSK6EVcVDQVi2-u8iuoJJ")
        for ul in uls:
            lis = ul.find_elements(By.CLASS_NAME, "_3hRXlwV68b7y5e5EjN2HQy")
            for li in lis:
                text = li.text.strip()
                if text:
                    print(f" - {text}")

driver.quit()
