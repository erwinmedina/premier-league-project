#!/usr/bin/env python3

# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file extracts the match stats info from Flashscore match-stats pages.
# Input: Excel file with column 'URLs' (links to each game)
# Output: Excel file with new columns:
    #   Ball Possession - Home, Ball Possession - Away,
    #   Total Shots - Home, Total Shots - Away,
    #   Shots on Target - Home, Shots on Target - Away,
    #   Corner Kicks - Home, Corner Kicks - Away,
    #   Offsides - Home, Offsides - Away,
    #   Free Kicks - Home, Free Kicks - Away,
    #   Fouls - Home, Fouls - Away

import time
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

# Additional optional webdrivers - keeping just in case.
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    WEBDRIVER_MANAGER = True
except Exception:
    WEBDRIVER_MANAGER = False

# canonical stat names (Title Case for output)
CANONICAL_STATS = [
    "Ball Possession",
    "Total Shots",
    "Shots on Target",
    "Corner Kicks",
    "Offsides",
    "Free Kicks",
    "Fouls"
]

# Aliases / variants to match the category found [like offside]
STAT_ALIASES = {
    "Ball Possession": ["ball possession"],
    "Total Shots": ["total shots"],
    "Shots on Target": ["shots on target"],
    "Corner Kicks": ["corner kicks"],
    "Offsides": ["offsides", "offside"],
    "Free Kicks": ["free kicks"],
    "Fouls": ["fouls"]
}

def get_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    
    # Additional webdrivers; allowing others to run the chromedriver and not experience issues running this file.
    try:
        if WEBDRIVER_MANAGER:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=opts)
        else:
            driver = webdriver.Chrome(options=opts)
        return driver
    except WebDriverException as e:
        raise RuntimeError("Could not start Chrome WebDriver. Ensure chromedriver is installed or install webdriver-manager.") from e

# Waits for any CSS selectors on the page to load thoroughly before attempting anything
def wait_for_any(driver, selectors, timeout=12):
    end = time.time() + timeout
    while time.time() < end:
        for sel in selectors:
            try:
                if driver.find_elements(By.CSS_SELECTOR, sel):
                    return True
            except Exception:
                pass
        time.sleep(0.25)
    return False

# Strips white space, and makes everything lowercase.
def normalize_text(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip().lower()

# Does the matching from alias/variant to the canonical/correct stat name.
def match_canonical(category_text):
    t = normalize_text(category_text)
    for canonical, aliases in STAT_ALIASES.items():
        for a in aliases:
            a_norm = normalize_text(a)
            if a_norm == t or a_norm in t or t in a_norm:
                return canonical
    return None

# Does the actual parsing of the stats page
def parse_stats_soup(soup):
    out = {}

    # find all stat rows with this particular selector.
    rows = soup.select("div.wcl-row_2oCpS")
    if not rows:
        # backup selectors, just in case. Doubt it hits this though.
        rows = soup.select("[data-analytics-context='tab-match-statistics'] .section div[class*='wcl-row']")

    for row in rows:
        category_element = row.select_one("div.wcl-category_6sT1J strong, div[class*='wcl-category'] strong, div[class*='wcl-category']")
        if not category_element:
            continue
        category_text = category_element.get_text(strip=True)
        canonical = match_canonical(category_text)
        if canonical is None:
            continue

        # ------------------ #
        # Home & Away Values #
        # ------------------ #

        # Try explicit home/away classes first
        home_val = None
        away_val = None
        home_candidate = row.select_one("div[class*='homeValue'] strong")
        away_candidate = row.select_one("div[class*='awayValue'] strong")
        
        # If we found the candidate, do the following.
        if home_candidate or away_candidate:
            home_val = home_candidate.get_text(strip=True) if home_candidate else None
            away_val = away_candidate.get_text(strip=True) if away_candidate else None
        
        # If we didn't find the candidate, check selector variants
        else:
            home_candidate = row.select_one(".wcl-homeValue_3Q-7P strong, .wcl-value_XJG99 .wcl-homeValue_3Q-7P strong")
            away_candidate = row.select_one(".wcl-awayValue_Y-QR1 strong, .wcl-value_XJG99 .wcl-awayValue_Y-QR1 strong")
            
            # Same as before
            if home_candidate or away_candidate:
                home_val = home_candidate.get_text(strip=True) if home_candidate else None
                away_val = away_candidate.get_text(strip=True) if away_candidate else None
            
            else:
                # Incase nothing is found: take first/last <strong> in the row
                strongs = row.select("strong")
                if strongs:
                    home_val = strongs[0].get_text(strip=True)
                    away_val = strongs[-1].get_text(strip=True) if len(strongs) > 1 else None

        # Starts to put this info away
        out[f"{canonical} - Home"] = home_val
        out[f"{canonical} - Away"] = away_val

    # Makes sure all canonical stats are present
    for stat in CANONICAL_STATS:
        out.setdefault(f"{stat} - Home", None)
        out.setdefault(f"{stat} - Away", None)

    return out

# ------------------------------------------------------------------------------- #
# This makes sure that the stats part of the URL is fully loaded before scraping. #
# ------------------------------------------------------------------------------- #
def scrape_stats_for_url(driver, url):
    
    driver.get(url)

    # Wait for stat rows to appear
    if not wait_for_any(driver, ["div.wcl-row_2oCpS", "[data-analytics-context='tab-match-statistics']"], timeout=15):
        print("warning: stats container not found")
        return {}

    # Wait until we have non-empty numbers for at least one key stat
    end_time = time.time() + 15
    while time.time() < end_time:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select("div.wcl-row_2oCpS strong")
        # if at least one value is non-empty, break.
        if any(strong.get_text(strip=True) for strong in rows):
            break
        time.sleep(0.3)

    # Final parse after ensuring numbers are present
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return parse_stats_soup(soup)


def main(infile, outfile, headless=True):

    df = pd.read_excel(infile, dtype=str)
    driver = get_driver(headless=headless)
    rows = []
    
    # Tells me the index / total, then scrapes the stats.
    for index, url in enumerate(df["URLS"].dropna().tolist(), start=1):
        print(f"[{index}/{len(df)}] scraping stats for: {url}")
        try:
            row = scrape_stats_for_url(driver, url)
            row["SourceURL"] = url
            rows.append(row)
        except Exception as e:
            print("Error:", e)
            rows.append({"SourceURL": url, "Error": str(e)})
        time.sleep(1)

    driver.quit()
    out_df = pd.DataFrame(rows)

    # Puts the columns in order.
    ordered_cols = ["SourceURL"]
    for stat in CANONICAL_STATS:
        ordered_cols.append(f"{stat} - Home")
        ordered_cols.append(f"{stat} - Away")

    out_df = out_df[ordered_cols]
    out_df.to_excel(outfile, index=False)
    print("Output file complete! Find it as:", outfile)

# Main bad boy that runs the entire file
if __name__ == "__main__":
    import sys
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) < 2:
        print("CMD Terminal Should Read: python3 {This Scripts Filepath} {InputFile} {OutputFile}")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], headless=True)

# USE THE FOLLOWING IN THE CMD TERMINAL TO RUN THIS
# python3 '/Users/erwinmedina/code/finalproject/Output Stats/Flashscore - Stats Scraper'.py input_urls_2024-2025-test.xlsx stats_test_output.xlsx