#!/usr/bin/env python3

# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file scrapes all of the incidents from Flashscore match-summary pages.
# All incidents range from: 
    # Yellow/Red Cards
    # Substitutions
    # Goals [Regular, Penalty, Own]
# The output that this creates is a list of items that look like this:
# ['<time> <EventType>_<Side> - <PlayerName> (AssistOrReason)']

import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Just driver stuff; allows this file to run without issues.
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    WEBDRIVER_MANAGER = True
except Exception:
    WEBDRIVER_MANAGER = False

def get_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    if WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=opts)
    return webdriver.Chrome(options=opts)

# This reads in the icon_div, and determines what type of event it is
def classify_event(icon_div):
    if not icon_div:
        return "Other"
    
    # Checks for Goals
    homeGoal = icon_div.find('div', class_="smv__incidentHomeScore")
    awayGoal = icon_div.find('div', class_="smv__incidentAwayScore")

    # Gets the SVG
    svg = icon_div.find("svg")
    
    # Checks if penalty was missed
    # Wanted, in case i want to check penalties given
    if svg:
        data_testid = svg.get("data-testid", "")
        if "penalty-missed" in data_testid:
            return "Penalty_Missed"

    # Checks if there was a goal
    if homeGoal or awayGoal:
        return "Goal"
    
    if not svg:
        return "Other"
    
    # Second Yellow
    title_tag = svg.find("title")
    if title_tag and "Yellow card / Red card" in title_tag.get_text(strip=True):
        return "Red_Card"

    # Gets the class of the SVG
    cls = svg.get("class") or ""
    cls_s = " ".join(cls) if isinstance(cls, (list, tuple)) else str(cls)
    cls_s = cls_s.lower()

    # Determines what to return
    if "yellow" in cls_s:
        return "Yellow"
    if "red" in cls_s:
        return "Red_Card"
    if "own" in cls_s:
        return "Own"
    if "sub" in cls_s:  # substitution
        return "Sub"
    if "var" in cls_s:
        return "VAR"
    return "Other"

# Simply parses through the html/soup that it collected
def parse_participant_rows(soup):
    results = []
    vs = soup.select_one("div.smv__verticalSections.section")
    if not vs:
        return results

    rows = vs.select("div.smv__participantRow")
    for row in rows:
        row_cls = " ".join(row.get("class", [])).lower()
        side = "Home" if "homeparticipant" in row_cls else "Away" if "awayparticipant" in row_cls else "Unknown"

        inc = row.select_one("div.smv__incident")
        if not inc:
            continue

        # time
        time_tag = inc.find("div", class_="smv__timeBox")
        time_text = time_tag.get_text(strip=True) if time_tag else ""

        # event type
        icon_div = inc.find("div", class_="smv__incidentIcon") or inc.find("div", class_="smv__incidentIconSub")
        event_type = classify_event(icon_div)

        # player
        player_tag = inc.select_one(".smv__playerName")
        player = player_tag.get_text(" ", strip=True) if player_tag else ""

        # assist/reason
        if (event_type != "Penalty_Missed"):
            extra_tag = inc.select_one(".smv__subIncident, .smv__assist")
            extra_text = extra_tag.get_text(" ", strip=True) if extra_tag else ""
            extra = f"({extra_text})" if extra_text else ""
        else:
            extra = ()

        # final string
        final = f"{time_text} {event_type}_{side} - {player}{extra}"
        results.append(final)

    return results

# Scrapes the html from the url and runs the parser to figure out the rest
def scrape_incidents_for_url(driver, url):
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.smv__verticalSections.section"))
        )
    except TimeoutException:
        return []

    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return parse_participant_rows(soup)

# This bad boy is the main function that runs the entire show #
def main(infile, outfile, headless=True):
    df = pd.read_excel(infile, dtype=str)
    driver = get_driver(headless=headless)
    rows = []
    try:
        urls = df["URLS"].dropna().tolist()
        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] {url}")
            try:
                incs = scrape_incidents_for_url(driver, url)
                rows.append({"SourceURL": url, "INC": str(incs)})
            except Exception as e:
                rows.append({"SourceURL": url, "INC": "[]", "Error": str(e)})
            time.sleep(0.5)
    finally:
        driver.quit()

    out_df = pd.DataFrame(rows)
    out_df.to_excel(outfile, index=False)
    print("Saved:", outfile)

if __name__ == "__main__":
    # main("input_urls_test.xlsx", "output_incidents_test.xlsx", headless=True)
    main("input_urls_random-test.xlsx", "output_incidents_random-test.xlsx", headless=True)
    # main("input_urls_2002-2003.xlsx", "output_incidents_2002-2003.xlsx", headless=True)
    # main("input_urls_2003-2004.xlsx", "output_incidents_2003-2004.xlsx", headless=True)
    # main("input_urls_2004-2005.xlsx", "output_incidents_2004-2005.xlsx", headless=True)
    # main("input_urls_2005-2006.xlsx", "output_incidents_2005-2006.xlsx", headless=True)
    # main("input_urls_2006-2007.xlsx", "output_incidents_2006-2007.xlsx", headless=True)
    # main("input_urls_2007-2008.xlsx", "output_incidents_2007-2008.xlsx", headless=True)
    # main("input_urls_2008-2009.xlsx", "output_incidents_2008-2009.xlsx", headless=True)
    # main("input_urls_2009-2010.xlsx", "output_incidents_2009-2010.xlsx", headless=True)
    # main("input_urls_2010-2011.xlsx", "output_incidents_2010-2011.xlsx", headless=True)
    # main("input_urls_2011-2012.xlsx", "output_incidents_2011-2012.xlsx", headless=True)
    # main("input_urls_2012-2013.xlsx", "output_incidents_2012-2013.xlsx", headless=True)
    # main("input_urls_2013-2014.xlsx", "output_incidents_2013-2014.xlsx", headless=True)
    # main("input_urls_2014-2015.xlsx", "output_incidents_2014-2015.xlsx", headless=True)
    # main("input_urls_2015-2016.xlsx", "output_incidents_2015-2016.xlsx", headless=True)
    # main("input_urls_2016-2017.xlsx", "output_incidents_2016-2017.xlsx", headless=True)
    # main("input_urls_2017-2018.xlsx", "output_incidents_2017-2018.xlsx", headless=True)
    # main("input_urls_2018-2019.xlsx", "output_incidents_2018-2019.xlsx", headless=True)
    # main("input_urls_2019-2020.xlsx", "output_incidents_2019-2020.xlsx", headless=True)
    # main("input_urls_2020-2021.xlsx", "output_incidents_2020-2021.xlsx", headless=True)
    # main("input_urls_2021-2022.xlsx", "output_incidents_2021-2022.xlsx", headless=True)
    # main("input_urls_2022-2023.xlsx", "output_incidents_2022-2023.xlsx", headless=True)
    # main("input_urls_2023-2024.xlsx", "output_incidents_2023-2024.xlsx", headless=True)
    # main("input_urls_2024-2025.xlsx", "output_incidents_2024-2025.xlsx", headless=True)