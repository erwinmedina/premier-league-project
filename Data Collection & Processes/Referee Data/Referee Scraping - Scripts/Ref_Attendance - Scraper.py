# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file collects all of the 'strong' tags in a certain location.
# Then returns the first and last value [ref, attendance].
# There is a second delay between requests to avoid suspicion.
# This is the fourth iteration of the file. 

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

df = pd.read_excel("urls.xlsx")
urls = df["URL"].tolist()

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

start_time = time.time()
results = []
total = len(urls)

for index, url in enumerate(urls, start=1):
    try:

        # Gives time elapsed, and which url we're on.
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        print(f"[{index}/{total}] - TIME: {minutes:02d}:{seconds:02d}")
        driver.get(url)
        
        # Wait until the divs are loaded.
        divs = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.wcl-infoValue_grawU"))
        )
        
        # Collect all <strong> text/tags in a specific div
        temp_results = [div.find_element(By.TAG_NAME, "strong").text.strip() for div in divs]
        
        # Grab first and last [ref, attendance]
        refereeName = temp_results[0]
        attendance = temp_results[-1].replace(" ", "")  # remove spaces
        
        # PUT IT ALL TOGETHER !
        results.append([refereeName, attendance, url])
        time.sleep(1) 
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
        results.append(["Error", "Error", url])

driver.quit()

# Save results to Excel
results_df = pd.DataFrame(results, columns=["Referee", "Attendance", "URL"])
results_df.to_excel("results.xlsx", index=False)

print("Scraping complete! Results saved to results.xlsx")
