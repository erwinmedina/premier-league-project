# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file extracts the summary info from Flashscore match-summary pages.
# Input: Excel file with column 'URLs' (links to each game)
# Output: Excel file with new columns:
    # HomeTeam, AwayTeam, Matchday, StartDateTime,
    # HomeTeamScore, AwayTeamScore, Referee, Attendance

#!/usr/bin/env python3
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

def get_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=opts)
    return driver

def parse_summary_soup(soup):
    out = {}

    # Teams
    teams = soup.select("a.participant__participantName")
    if len(teams) >= 2:
        out["HomeTeam"] = teams[0].get_text(strip=True)
        out["AwayTeam"] = teams[1].get_text(strip=True)

    # Matchday / Round
    matchday_element = soup.select_one("ol.wcl-breadcrumbList_lC9sI li:last-of-type a span")
    if matchday_element:
        out["Matchday"] = matchday_element.get_text(strip=True)

    # Start time/date
    start_time_element = soup.select_one("div.duelParticipant__startTime > div")
    if start_time_element:
        out["StartDateTime"] = start_time_element.get_text(strip=True)

    # Scores
    score_spans = soup.select("div.detailScore__wrapper span")
    if len(score_spans) >= 2:
        out["HomeTeamScore"] = score_spans[0].get_text(strip=True)
        out["AwayTeamScore"] = score_spans[-1].get_text(strip=True)

    # Attendance & Referee (label-based search)
    label_wrappers = soup.select("div.wcl-infoLabelWrapper_DXbvw")
    for w in label_wrappers:
        label_el = w.select_one(".wcl-overline_uwiIT, .wcl-infoLabel_xPJVi, span")
        label = label_el.get_text(strip=True) if label_el else w.get_text(strip=True)
        label = label.rstrip(":").lower()
        value_element = w.find_next_sibling(class_="wcl-infoValue_grawU")
        if value_element:
            strong_element = value_element.find("strong")
            val = strong_element.get_text(strip=True) if strong_element else value_element.get_text(strip=True)
            if "attendance" in label:
                out["Attendance"] = val
            elif "referee" in label:
                out["Referee"] = val

    return out

def scrape_summary(driver, url):
    driver.get(url)
    time.sleep(2)  # This timer lets the javascript load.
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return parse_summary_soup(soup)

def main(input_file, output_file, headless=True):
    df = pd.read_excel(input_file, dtype=str)

    driver = get_driver(headless=headless)
    results = []
    # Needed to tell me which iteration it was on so I knew it was doing its job.
    for index, url in enumerate(df["URLS"].dropna(), start=1):
        print(f"[{index}] Scraping {url} ...")
        try:
            data = scrape_summary(driver, url)
            data["SourceURL"] = url
            results.append(data)
        except Exception as e:
            print(f"Error: {e}")
            results.append({"SourceURL": url, "Error": str(e)})

    # Wraps up, closes, saves.
    driver.quit()
    out_df = pd.DataFrame(results)
    out_df.to_excel(output_file, index=False)
    print(f"Saved {output_file}")

# Basically, runs the file. Use long string below as basis to run entire script
# input_url file, and output file will be created/outputed into this folder.
if __name__ == "__main__":
    import sys
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) < 2:
        print("Usage: python3 '/Users/erwinmedina/code/finalproject/Output Summary/Flashscore - Summary Scraper.py' input_urls_2024-2025-test.xlsx output.xlsx")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], headless=True)