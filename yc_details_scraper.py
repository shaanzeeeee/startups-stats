"""
YC Company Details Scraper
==========================
Enriches yc_companies.csv with: Founded, Team Size, Company Status.

- Team Size: pulled from the Algolia API data (already in checkpoints/)
- Founded & Status: scraped from each company's YC profile page

Checkpoint: saves progress every 50 companies for resume support.

Usage: python yc_details_scraper.py
"""

import json, re, time, os, sys
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- Settings ---
INPUT_CSV = "yc_companies.csv"
OUTPUT_CSV = "yc_companies.csv"
CHECKPOINT_CSV = "yc_details_checkpoint.csv"
CHECKPOINT_FOLDER = "checkpoints"
DELAY = 0.5                  # seconds between page requests
SAVE_EVERY = 50              # save checkpoint every N companies

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
}


# ============================================================
# STEP 1: Load Team Size from Algolia cache (fast, no scraping)
# ============================================================
def load_team_sizes():
    """
    Reads the Algolia checkpoint JSONs to build a {company_name: team_size} map.
    This data was already fetched by yc_scraper.py — no extra requests needed.
    """
    team_sizes = {}

    if not os.path.exists(CHECKPOINT_FOLDER):
        print("No checkpoints/ folder found. Team Size will be scraped from pages.")
        return team_sizes

    for filename in os.listdir(CHECKPOINT_FOLDER):
        if not filename.startswith("batch_") or not filename.endswith(".json"):
            continue

        filepath = os.path.join(CHECKPOINT_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Skip files that aren't batch data dicts (e.g. batch_names.json is a list)
        if not isinstance(data, dict):
            continue

        for hit in data.get("hits", []):
            name = hit.get("name", "")
            size = hit.get("team_size", "")
            if name and size:
                team_sizes[name] = str(size)

    print(f" Loaded team sizes for {len(team_sizes)} companies from Algolia cache.")
    return team_sizes


# ============================================================
# STEP 2: Scrape Founded & Status from a company profile page
# ============================================================
def scrape_page_details(url):
    """
    Visits a company's YC profile page and extracts Founded and Status.
    Also gets Team Size from the page as a fallback.
    """
    result = {"Founded": "", "Team Size (page)": "", "Company Status": ""}

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return result

        soup = BeautifulSoup(resp.text, "html.parser")

        # Each detail row: <div class="flex flex-row justify-between">
        #                     <span>Label:</span> <span>Value</span>
        #                  </div>
        for row in soup.find_all("div", class_="flex flex-row justify-between"):
            spans = row.find_all("span", recursive=False)
            if len(spans) < 2:
                continue

            label = spans[0].get_text(strip=True)
            value = spans[1].get_text(strip=True)

            if label == "Founded:":
                result["Founded"] = value
            elif label == "Team Size:":
                result["Team Size (page)"] = value
            elif label == "Status:":
                result["Company Status"] = value

    except Exception as e:
        print(f" Error: {e}")

    return result


# ============================================================
# MAIN
# ============================================================
def main():
    print("\n YC Company Details Scraper\n")

    # Load the CSV
    if not os.path.exists(INPUT_CSV):
        print(f" {INPUT_CSV} not found. Run yc_scraper.py first.")
        sys.exit(1)

    df = pd.read_csv(INPUT_CSV)
    print(f" Loaded {len(df)} companies from {INPUT_CSV}")

    # STEP 1: Get team sizes from Algolia cache (instant, no HTTP requests)
    team_sizes = load_team_sizes()

    # STEP 2: Check for resume checkpoint
    start_from = 0
    if os.path.exists(CHECKPOINT_CSV):
        df = pd.read_csv(CHECKPOINT_CSV)
        # Count rows that already have Founded filled
        filled = df["Founded"].notna() & (df["Founded"].astype(str).str.strip() != "")
        start_from = filled.sum()
        print(f" Resuming from row {start_from}/{len(df)}")

    # Add new columns if they don't exist
    for col in ["Founded", "Team Size", "Company Status"]:
        if col not in df.columns:
            df[col] = ""

    # STEP 3: Fill Team Size from Algolia data (no scraping needed)
    filled_count = 0
    for i in range(len(df)):
        name = df.at[i, "Company Name"]
        if name in team_sizes:
            df.at[i, "Team Size"] = team_sizes[name]
            filled_count += 1
    print(f" Filled Team Size for {filled_count}/{len(df)} companies from Algolia data.")

    # STEP 4: Scrape Founded & Status from each company page
    total = len(df)
    print(f"\n📡 Scraping Founded & Status for {total - start_from} remaining companies...\n")

    for i in range(start_from, total):
        name = df.at[i, "Company Name"]
        url = df.at[i, "Company Link"]

        # Skip if already scraped
        if pd.notna(df.at[i, "Founded"]) and str(df.at[i, "Founded"]).strip() != "":
            continue

        print(f"   [{i+1}/{total}] {name}...", end=" ")
        details = scrape_page_details(url)

        df.at[i, "Founded"] = details["Founded"]
        df.at[i, "Company Status"] = details["Company Status"]

        # Use page Team Size as fallback if Algolia didn't have it
        if str(df.at[i, "Team Size"]).strip() in ("", "nan"):
            df.at[i, "Team Size"] = details["Team Size (page)"]

        print(f"Founded: {details['Founded']} | Status: {details['Company Status']}")

        # Checkpoint
        if (i + 1) % SAVE_EVERY == 0:
            df.to_csv(CHECKPOINT_CSV, index=False, encoding="utf-8-sig")
            print(f"   💾 Checkpoint saved ({i+1}/{total})")

        time.sleep(DELAY)

    # Save final result
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\n Done! Saved to {OUTPUT_CSV}")

    if os.path.exists(CHECKPOINT_CSV):
        os.remove(CHECKPOINT_CSV)

    # Summary
    print(f"\n Summary:")
    print(f"   Founded filled   : {(df['Founded'].astype(str).str.strip() != '').sum()}/{total}")
    print(f"   Team Size filled : {(df['Team Size'].astype(str).str.strip() != '').sum()}/{total}")
    print(f"   Status filled    : {(df['Company Status'].astype(str).str.strip() != '').sum()}/{total}")


if __name__ == "__main__":
    main()
