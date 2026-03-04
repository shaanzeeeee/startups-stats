# Y Combinator Startups Statistics & Scraping Project

## Project Overview
This project focuses on extracting and enriching a comprehensive dataset of ~5,700 startups from the **Y Combinator (YC) Directory**. As a data analyst, the primary goal was to build a reliable, clean, and high-integrity dataset that captures the evolution of the startup ecosystem across multiple batches and industries.

The dataset provides insights into company growth (Team Size), geographic distribution, and operational status (Active vs. Inactive).

## Data Analyst's Perspective
From a data analysis standpoint, this project addresses several critical challenges:
- **Data Completeness**: Standard UI scraping often hits pagination limits (usually 1,000 results). By pivoting to the underlying Algolia search API, we achieved 100% coverage of all 5,700+ companies.
- **Data Integrity**: Implementing a batch-by-batch extraction system ensured that no records were duplicated or missed during the process.
- **Enrichment**: A two-stage scraping process was used to first gather structural data (API) and then enrich it with deep page-level details (HTML parsing).

## The Scraping Process

### Stage 1: API-Driven Extraction (`yc_scraper.py`)
Instead of traditional "point-and-click" scraping, this script interacts directly with YC's search engine (Algolia).
1. **API Key Discovery**: Uses Selenium (headless) to visit the YC directory and capture the short-lived `x-algolia-api-key` from network logs.
2. **Batch Discovery**: Queries the API to identify all YC batches (e.g., "Winter 2024", "Summer 2005").
3. **Batch-by-Batch Fetching**: Iterates through each batch to retrieve unique company records. This bypasses the 1,000-result limit imposed on global searches.
4. **Checkpoint System**: Saves results for each batch to JSON in the `checkpoints/` folder, allowing for resumes if interrupted.

### Stage 2: Deep Enrichment (`yc_details_scraper.py`)
Once the base list is created, we perform high-resolution scraping of individual company profile pages.
- **Technology**: Uses `BeautifulSoup` and `Requests` with randomized delays to respect robots.txt and server load.
- **Fields Extracted**: 
    - **Founded**: Extracting the exact year the company started.
    - **Status**: Identifying if the company is "Active", "Acquired", or "Inactive".
    - **Team Size**: Validating team size data from the profile pages.

## Project Structure & Content
A professional project repository should include:
- **`README.md`**: Project context, methodology, and documentation (this file).
- **`requirements.txt`**: List of Python dependencies for reproducibility.
- **`yc_scraper.py`**: The core API extraction script.
- **`yc_details_scraper.py`**: The enrichment script for profile-level data.
- **`.gitignore`**: Ensuring cache, temporary checkpoints, and secrets are not pushed to Git.
- **`yc_companies.csv`**: The final output dataset.

## Data Dictionary (`yc_companies.csv`)

| Field | Description | Source |
| :--- | :--- | :--- |
| **Company Name** | Legal or trading name of the startup. | Algolia API |
| **Batch** | The YC funding cycle (e.g., W24, S05). | Algolia API |
| **Industry / Sub Industry**| Functional sector of the company. | Algolia API |
| **Company Country** | Country of headquarters. | Algolia API (Parsed) |
| **Founded** | The year the company was established. | Profile Page |
| **Team Size** | Number of employees. | API / Profile Page |
| **Company Status** | Current status (Active, Acquired, etc.). | Profile Page |
| **Company Link** | URL to the YC profile page. | Generated Slug |

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the base scraper:
   ```bash
   python yc_scraper.py
   ```
3. Run the enrichment scraper:
   ```bash
   python yc_details_scraper.py
   ```

---
*Note: This scraper was built for educational purposes and respects YC's directory structure and robots.txt. Always ensure ethical scraping practices.*
