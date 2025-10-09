# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# All this file is meant to do is scrape the entire page provided by the url.
# I wanted to do this so that i can understand a better approach on how to
# scrape the information i was looking for versus looking at the DOM.

from playwright.sync_api import sync_playwright

url = "https://www.flashscore.com/match/football/MgRapPRs/#/match-summary/match-statistics/0"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # wait until most network calls finish
    page.goto(url, wait_until="networkidle")  
    
    # fully rendered HTML
    html_content = page.content()  
    with open("flashscore_page_statspage_2.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    browser.close()

print("HTML saved to flashscore_page.html")
