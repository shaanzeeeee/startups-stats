"""Debug: dump ALL label-value pairs from several company pages."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

urls = [
    "https://www.ycombinator.com/companies/doordash",
    "https://www.ycombinator.com/companies/careforce",
    "https://www.ycombinator.com/companies/canvas-12",
    "https://www.ycombinator.com/companies/ember-6",
]

for url in urls:
    name = url.split("/")[-1]
    resp = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.find_all("div", class_="flex flex-row justify-between")
    print(f"\n=== {name} ({len(rows)} rows) ===")
    for row in rows:
        spans = row.find_all("span", recursive=False)
        if len(spans) >= 2:
            print(f"  '{spans[0].get_text(strip=True)}' → '{spans[1].get_text(strip=True)}'")
        else:
            # Check for any text content
            text = row.get_text(strip=True)[:100]
            print(f"  (non-standard) → '{text}'")
