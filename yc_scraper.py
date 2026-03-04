"""
YC Companies Scraper
====================
Scrapes all ~5,700 startups from https://www.ycombinator.com/companies
into a CSV file with: Company Name, Address, Country, Link, Industry, Batch, Sub Industry.

How it works:
  1. Opens YC website with Selenium to grab the API key
  2. Discovers all batch names (e.g. "Summer 2023") via the API
  3. Fetches companies batch-by-batch (each batch < 1000 companies)
  4. Saves everything to yc_companies.csv

Checkpoint system: each batch is saved as JSON — re-run skips already-fetched batches.
robots.txt: only accesses /companies (allowed), never uses query params (disallowed).
"""

import json, re, sys, time, os
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Settings ---
WEBSITE_URL = "https://www.ycombinator.com/companies"
OUTPUT_FILE = "yc_companies.csv"
CHECKPOINT_FOLDER = "checkpoints"
ALGOLIA_APP_ID = "45BWZJ1SGC"
ALGOLIA_INDEX = "YCCompany_production"
ALGOLIA_API_URL = f"https://{ALGOLIA_APP_ID.lower()}-dsn.algolia.net/1/indexes/*/queries"
BACKUP_API_KEY = (
    "ZjA3NWMwMmNhMzEwZmMxOThkZDlkMjFmNDAwNTNjNjdkZjdhNWJkOWRjMThiODQwMjUyZTVk"
    "YjA4YjFlMmU2YnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMi"
    "UyQyUyMllDQ29tcGFueV9CeV9MYXVuY2hfRGF0ZV9wcm9kdWN0aW9uJTIyJTVEJnRhZ0ZpbHRl"
    "cnM9JTVCJTIyeWNkY19wdWJsaWMlMjIlNUQmYW5hbHl0aWNzVGFncz0lNUIlMjJ5Y2RjJTIyJT"
    "VE"
)


# --- Helper: send a query to the Algolia API ---
def algolia_query(api_key, params):
    """Sends a search request to Algolia and returns the result."""
    headers = {
        "x-algolia-api-key": api_key,
        "x-algolia-application-id": ALGOLIA_APP_ID,
        "Content-Type": "application/json",
    }
    body = {"requests": [{"indexName": ALGOLIA_INDEX, "params": params}]}
    resp = requests.post(ALGOLIA_API_URL, json=body, headers=headers)
    resp.raise_for_status()
    return resp.json()["results"][0]


# --- Helper: load/save JSON checkpoint ---
def load_checkpoint(filename):
    """Returns saved JSON data if checkpoint exists, else None."""
    path = os.path.join(CHECKPOINT_FOLDER, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_checkpoint(filename, data):
    """Saves data as JSON checkpoint."""
    os.makedirs(CHECKPOINT_FOLDER, exist_ok=True)
    path = os.path.join(CHECKPOINT_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# ============================================================
# STEP 1: Get API key from YC website using Selenium
# ============================================================
def get_api_key():
    """Opens YC in a hidden browser and captures the Algolia API key."""

    # Check cache first
    cached = load_checkpoint("api_key.json")
    if cached:
        print("✅ API key loaded from cache.")
        return cached["api_key"]

    print("Opening YC website to extract API key...")

    # Launch headless Chrome
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1920,1080")
    opts.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )

    api_key = None
    try:
        browser.get(WEBSITE_URL)
        # Wait for company cards to load
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*='_company_']"))
        )
        print("Page loaded. Scanning network logs...")

        # Search network logs for the Algolia API key
        for entry in browser.get_log("performance"):
            msg = json.loads(entry["message"])["message"]
            if msg.get("method") == "Network.requestWillBeSent":
                url = msg["params"]["request"].get("url", "")
                if "algolia.net" in url:
                    key = msg["params"]["request"].get("headers", {}).get("x-algolia-api-key")
                    if key:
                        api_key = key
                        print("✅ API key extracted!")
                        break
    finally:
        browser.quit()

    if not api_key:
        print("Using backup API key.")
        api_key = BACKUP_API_KEY

    save_checkpoint("api_key.json", {"api_key": api_key})
    return api_key


# ============================================================
# STEP 2: Discover all YC batch names
# ============================================================
def get_batch_names(api_key):
    """Fetches all batch names (e.g. 'Summer 2023') via faceted search."""

    cached = load_checkpoint("batch_names.json")
    if cached:
        print(f"Loaded {len(cached)} batch names from cache.")
        return cached

    print("Discovering batch names...")
    result = algolia_query(api_key, "hitsPerPage=0&facets=batch&query=")
    batch_counts = result.get("facets", {}).get("batch", {})
    batch_names = sorted(batch_counts.keys())

    print(f"Found {len(batch_names)} batches ({sum(batch_counts.values())} companies total)")
    save_checkpoint("batch_names.json", batch_names)
    time.sleep(1)
    return batch_names


# ============================================================
# STEP 3: Fetch all companies batch-by-batch
# ============================================================
def fetch_all_companies(api_key, batch_names):
    """Queries each batch individually and combines all results."""

    all_companies = []

    for i, batch in enumerate(batch_names, 1):
        safe_name = re.sub(r'[^\w\-]', '_', batch)
        cached = load_checkpoint(f"batch_{safe_name}.json")

        if cached:
            companies = cached.get("hits", [])
            print(f"   [{i}/{len(batch_names)}] {batch}: {len(companies)} (cached)")
        else:
            print(f"   [{i}/{len(batch_names)}] {batch}...", end=" ")
            params = f"hitsPerPage=1000&page=0&query=&facetFilters=%5B%22batch%3A{batch}%22%5D"
            result = algolia_query(api_key, params)
            companies = result.get("hits", [])
            save_checkpoint(f"batch_{safe_name}.json", {"batch": batch, "hits": companies})
            print(f"→ {len(companies)} companies")
            time.sleep(1)

        all_companies.extend(companies)

    print(f"\nTotal fetched: {len(all_companies)} companies")
    return all_companies


# ============================================================
# STEP 4: Build a clean DataFrame
# ============================================================
def create_dataframe(all_companies):
    """Converts raw API data into a structured pandas DataFrame."""

    rows = []
    for i, c in enumerate(all_companies, 1):
        # Get address and extract country (last part after comma)
        address = c.get("all_locations", "")
        if isinstance(address, list):
            address = "; ".join(address)
        country = ""
        if address:
            parts = [p.strip() for p in address.split(";")[0].split(",")]
            country = parts[-1]

        slug = c.get("slug", "")
        rows.append({
            "Index": i,
            "Company Name": c.get("name", ""),
            "Company Address": address,
            "Company Country": country,
            "Company Link": f"https://www.ycombinator.com/companies/{slug}" if slug else "",
            "Industry": c.get("industry", ""),
            "Batch": c.get("batch", ""),
            "Sub Industry": c.get("subindustry", ""),
        })

    df = pd.DataFrame(rows)
    print(f"DataFrame: {len(df)} rows × {len(df.columns)} columns")
    return df


# ============================================================
# STEP 5: Save CSV and show summary
# ============================================================
def save_results(df):
    """Saves DataFrame to CSV and prints a summary."""

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 50}")
    print(f" Saved to: {OUTPUT_FILE}")
    print(f" Companies: {len(df):,} | Countries: {df['Company Country'].nunique()}")
    print(f" Batches: {df['Batch'].nunique()} | Industries: {df['Industry'].nunique()}")
    print(f"{'=' * 50}")
    print(f"\nFirst 10 rows:\n")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print(df.head(10).to_string(index=False))


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("\n YC Companies Scraper\n")

    api_key = get_api_key()                                # Step 1
    batch_names = get_batch_names(api_key)                 # Step 2
    all_companies = fetch_all_companies(api_key, batch_names)  # Step 3

    if not all_companies:
        print("No companies fetched!"); sys.exit(1)

    df = create_dataframe(all_companies)                   # Step 4
    save_results(df)                                       # Step 5

    print("\n Done!")
