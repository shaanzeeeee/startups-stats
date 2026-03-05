# Y Combinator Startups Statistics & Scraping Project

## Project Overview
This project focuses on extracting and enriching a comprehensive dataset of **~5,700 startups** from the **Y Combinator (YC) Directory**. My primary goal was to build a reliable, clean, and high-integrity dataset that captures the evolution of the startup ecosystem across multiple batches and industries.

The dataset provides insights into company growth (Team Size), geographic distribution, and operational status (Active vs. Inactive).

From a data analysis standpoint, this project addresses several critical challenges:
* **Data Completeness**: Standard UI scraping often hits pagination limits (usually 1,000 results). By pivoting to the underlying Algolia search API, we achieved 100% coverage of all 5,700+ companies.
* **Data Integrity**: Implementing a batch-by-batch extraction system ensured that no records were duplicated or missed during the process.
* **Enrichment**: A two-stage scraping process was used to first gather structural data (API) and then enrich it with deep page-level details (HTML parsing).

---

## Dashboard & Visualizations
The final dataset was analyzed and visualized in Tableau to uncover trends in the startup landscape. 

**View the Interactive Dashboard here:** [**Startup Stats on Tableau Public**](https://public.tableau.com/app/profile/md.mahinuzzaman.shaan/viz/startups-stats/StartupStats)

![**Full Dashboard Overview**](https://github.com/user-attachments/assets/ea76850a-d721-4d13-94f7-91eb77e2d1e1)

---

## Key Insights

![**Main Insights Panel**](https://github.com/user-attachments/assets/343d4546-5c6e-4c96-9cf9-b17d3c55d760)

### 1. Geographical Concentration
![**Geographical Concentration Map**](https://github.com/user-attachments/assets/ede107f5-25e7-4447-8793-35cda03903d6)

When I look at the whole world map, it’s honestly crazy how much the US dominates the entire startup scene. Even though people always talk about how you can start a company from a laptop anywhere, the data shows that the US is still the main hub for tech. Within the US, San Francisco and New York are the absolute hotspots, with San Francisco alone making up about **43% of all the companies** in the dataset. It basically proves to me that even in a digital world, if you're starting a company, you still want to be physically located right where all the top investors and tech talent are hanging out.

### 2. Dominant Industry Shift
![**Industry Shift Trends**](https://github.com/user-attachments/assets/850d0ba0-bb0f-4ee2-ac8d-1451e8d7beac)

I noticed a really interesting change when looking at how industries have shifted over the years. Back in the early days of YC, there were a lot more apps being built for regular people to use, but now it seems like almost everything has moved toward **B2B and SaaS**. It feels like the "easy" consumer apps have already been made, so now most founders are building complex software and tools for other businesses to use. This indicates to me that the startup world is maturing, and founders are focusing more on building stable products that other companies actually need to pay for to stay in business.

### 3. Remote Trend
![**Remote vs Office Trends**](https://github.com/user-attachments/assets/922b151a-4719-4e67-8a53-36be55b48138)

The whole remote work thing isn’t just a temporary phase that happened a few years ago; it actually seems to be sticking around as a new normal. I saw a giant spike in 2021 when everyone was stuck at home, but even though it’s dropped a bit since then, **about 30% of new startups** are still choosing to be remote. This tells me that a lot of founders realized they can hire the smartest people from all over the world without making them move to an expensive city. It’s definitely not the "office-only" world it used to be back in the early 2010s.

### 4. Survival vs. Acquisition Rate
![**Survival and Acquisition Cohorts**](https://github.com/user-attachments/assets/9b78b883-d8e7-4e73-8f64-1e2e55dffd33)

This chart taught me that I have to be really patient when looking at how successful a startup batch actually is. The new groups from 2024 look amazing because they have like a 95% survival rate, but that’s really just because they haven't been around long enough to fail yet. When I look at the older groups from ten or fifteen years ago, I can see the "true" story where the **survival rate settles around 70%**. It shows me that it usually takes a full decade for a company to either get bought out, go public, or unfortunately run out of money.

### 5. Year-Over-Year Growth
![**YoY Growth by Technology**](https://github.com/user-attachments/assets/4bdb9ca7-4ffe-44c7-a86f-33142c0ed4bb)

The growth chart for **AI** is probably the most insane thing I found in the whole project. While normal software and SaaS have stayed pretty steady for a long time, the growth line for AI just shoots straight up like a rocket starting around late 2022. It indicates to me that AI isn't just a small niche or a passing trend anymore. It’s basically becoming the required baseline for almost every single company I see getting started today, and it’s growing way faster than any other category in YC history.

### 6. Team Size Trend
![**Average Team Size Evolution**](https://github.com/user-attachments/assets/a427642e-660e-48c4-bba1-40e04e0311f5)

I was really surprised to see that the actual number of people it takes to start a company is getting much smaller. Back in 2018, the average team size was much higher, but now it’s usually just a tiny group of **2 or 3 founders**. With all the new AI coding tools and automated software available now, I think a really small, smart team can do today what used to take a whole office full of people. It shows me that startups are becoming way more efficient and can do a lot more with a lot less headcount.

### 7. Risk vs. Reward (Sectors)
![**Sector Risk/Reward Scatter Plot**](https://github.com/user-attachments/assets/ede107f5-25e7-4447-8793-35cda03903d6)

This plot is great because it shows me exactly which industries are total gambles and which ones are more like "safe" bets. I saw that stuff like **social media apps** have a super high failure rate of over 50%, which is honestly pretty scary for a founder. On the other hand, healthcare and industrial startups seem to have a much better chance of actually going public. It indicates to me that while social apps might be easier to start, the harder industries like biotech actually have a much clearer path to becoming a huge, public company.

---

## The Scraping Process

### Stage 1: API-Driven Extraction (`yc_scraper.py`)
Instead of traditional "point-and-click" scraping, this script interacts directly with YC's search engine (**Algolia**).
1.  **API Key Discovery**: Uses Selenium (headless) to visit the YC directory and capture the short-lived `x-algolia-api-key` from network logs.
2.  **Batch Discovery**: Queries the API to identify all YC batches (e.g., "Winter 2024", "Summer 2005").
3.  **Batch-by-Batch Fetching**: Iterates through each batch to retrieve unique company records. This bypasses the 1,000-result limit imposed on global searches.
4.  **Checkpoint System**: Saves results for each batch to JSON in the `checkpoints/` folder, allowing for resumes if interrupted.

### Stage 2: Deep Enrichment (`yc_details_scraper.py`)
Once the base list is created, we perform high-resolution scraping of individual company profile pages.
* **Technology**: Uses `BeautifulSoup` and `Requests` with randomized delays to respect `robots.txt` and server load.
* **Fields Extracted**: 
    * **Founded**: Extracting the exact year the company started.
    * **Status**: Identifying if the company is "Active", "Acquired", or "Inactive".
    * **Team Size**: Validating team size data from the profile pages.

---

## Project Structure
* `yc_scraper.py`: The core API extraction script.
* `yc_details_scraper.py`: The enrichment script for profile-level data.
* `yc_companies.csv`: The final output dataset.
* `requirements.txt`: List of Python dependencies for reproducibility.
* `.gitignore`: Ensuring cache, temporary checkpoints, and secrets are not pushed to Git.

---

## Data Dictionary (`yc_companies.csv`)

| Field | Description | Source |
| :--- | :--- | :--- |
| **Company Name** | Legal or trading name of the startup. | Algolia API |
| **Batch** | The YC funding cycle (e.g., W24, S05). | Algolia API |
| **Industry** | Functional sector of the company. | Algolia API |
| **Company Country** | Country of headquarters. | Algolia API (Parsed) |
| **Founded** | The year the company was established. | Profile Page |
| **Team Size** | Number of employees. | API / Profile Page |
| **Company Status** | Current status (Active, Acquired, etc.). | Profile Page |
| **Company Link** | URL to the YC profile page. | Generated Slug |

---

## How to Run

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the base scraper**:
    ```bash
    python yc_scraper.py
    ```

3.  **Run the enrichment scraper**:
    ```bash
    python yc_details_scraper.py
    ```

---
*Note: This scraper was built for educational purposes and respects YC's directory structure and robots.txt. Always ensure ethical scraping practices.*
