## Startups Stats

## Project Overview
This project provides an end-to-end pipeline for extracting, cleaning, and analyzing data from the **Y Combinator (YC) Directory**. By bypassing standard UI limitations through direct API interaction and targeted HTML parsing, we have compiled a dataset of **5,800+ startups** with 100% coverage.

The analysis focuses on historical evolution, industry shifts, and survival cohorts, offering a high-integrity view of the startup landscape from 2005 to 2024.

---

## Interactive Dashboard
The final dataset is visualized in an interactive Tableau dashboard to surface multi-dimensional trends in growth, geography, and survival.

**Dashboard Link:** [**Visualizing the YC Startup Ecosystem on Tableau Public**](https://public.tableau.com/app/profile/md.mahinuzzaman.shaan/viz/startups-stats/StartupStats)

![Full Dashboard Overview](https://github.com/user-attachments/assets/ea76850a-d721-4d13-94f7-91eb77e2d1e1)

---

## Key Analytical Insights

### 1. Global Hub Concentration
When I look at the whole world map, it’s honestly crazy how much the US dominates the entire startup scene. Even though people always talk about how you can start a company from a laptop anywhere, the data shows that the US is still the main hub for tech. Within the US, San Francisco and New York are the absolute hotspots, with San Francisco alone making up about **43% of all the companies** in the dataset. It basically proves to me that even in a digital world, if you're starting a company, you still want to be physically located right where all the top investors and tech talent are hanging out.

![Geographical Concentration Map](https://github.com/user-attachments/assets/343d4546-5c6e-4c96-9cf9-b17d3c55d760)

### 2. Strategic Shift to B2B and SaaS
I noticed a really interesting change when looking at how industries have shifted over the years. Back in the early days of YC, there were a lot more apps being built for regular people to use, but now it seems like almost everything has moved toward **B2B and SaaS**. It feels like the "easy" consumer apps have already been made, so now most founders are building complex software and tools for other businesses to use. This indicates to me that the startup world is maturing, and founders are focusing more on building stable products that other companies actually need to pay for to stay in business.

![Industry Shift Trends](https://github.com/user-attachments/assets/ede107f5-25e7-4447-8793-35cda03903d6)

### 3. Sustainability of Remote Operations
The whole remote work thing isn’t just a temporary phase that happened a few years ago; it actually seems to be sticking around as a new normal. I saw a giant spike in 2021 when everyone was stuck at home, but even though it’s dropped a bit since then, **about 30% of new startups** are still choosing to be remote. This tells me that a lot of founders realized they can hire the smartest people from all over the world without making them move to an expensive city. It’s definitely not the "office-only" world it used to be back in the early 2010s.
![Remote vs Office Trends](https://github.com/user-attachments/assets/850d0ba0-bb0f-4ee2-ac8d-1451e8d7beac)




### 4. Survival vs. Acquisition Rate
This chart taught me that I have to be really patient when looking at how successful a startup batch actually is. The new groups from 2024 look amazing because they have like a 95% survival rate, but that’s really just because they haven't been around long enough to fail yet. When I look at the older groups from ten or fifteen years ago, I can see the "true" story where the **survival rate settles around 70%**. It shows me that it usually takes a full decade for a company to either get bought out, go public, or unfortunately run out of money.
![Survival and Acquisition Cohorts](https://github.com/user-attachments/assets/922b151a-4719-4e67-8a53-36be55b48138)


### 5. Year-Over-Year Growth
The growth chart for **AI** is probably the most insane thing I found in the whole project. While normal software and SaaS have stayed pretty steady for a long time, the growth line for AI just shoots straight up like a rocket starting around late 2022. It indicates to me that AI isn't just a small niche or a passing trend anymore. It’s basically becoming the required baseline for almost every single company I see getting started today, and it’s growing way faster than any other category in YC history.
![YoY Growth by Technology](https://github.com/user-attachments/assets/9b78b883-d8e7-4e73-8f64-1e2e55dffd33)

### 6. Team Size Trend

I was really surprised to see that the actual number of people it takes to start a company is getting much smaller. Back in 2018, the average team size was much higher, but now it’s usually just a tiny group of **2 or 3 founders**. With all the new AI coding tools and automated software available now, I think a really small, smart team can do today what used to take a whole office full of people. It shows me that startups are becoming way more efficient and can do a lot more with a lot less headcount.
![Average Team Size Evolution](https://github.com/user-attachments/assets/4bdb9ca7-4ffe-44c7-a86f-33142c0ed4bb)


### 7. Risk vs. Reward (Sectors)

This plot is great because it shows me exactly which industries are total gambles and which ones are more like "safe" bets. I saw that stuff like **social media apps** have a super high failure rate of over 50%, which is honestly pretty scary for a founder. On the other hand, healthcare and industrial startups seem to have a much better chance of actually going public. It indicates to me that while social apps might be easier to start, the harder industries like biotech actually have a much clearer path to becoming a huge, public company.
![**Sector Risk/Reward Scatter Plot**](https://github.com/user-attachments/assets/a427642e-660e-48c4-bba1-40e04e0311f5)

---

## Technical Architecture

### Stage 1: API-Driven Extraction (`yc_scraper.py`)
This stage bypasses traditional UI scraping to prevent data loss from pagination limits.
- **API Interception**: Uses Selenium to capture short-lived `x-algolia-api-key` headers from network traffic.
- **Facet Discovery**: Identifies all YC batches (e.g., Summer 2005) to scope queries.
- **Batch Processing**: Fetches records batch-by-batch, ensuring 100% coverage of the directory.
- **Resilience**: Implements a JSON-based checkpoint system to allow for resuming interrupted operations.

### Stage 2: Deep Enrichment (`yc_details_scraper.py`)
Enriches the structural data with high-resolution details via individual profile parsing.
- **HTML Parsing**: Uses BeautifulSoup to extract fields not available in the primary API.
- **Adaptive Delays**: Implements randomized wait times to respect server load and `robots.txt` guidelines.
- **Data Points**: Extracts exact founding year, operational status, and verified team sizes.

---

## Data Dictionary (`yc_companies.csv`)

| Field | Description | Source |
| :--- | :--- | :--- |
| **Company Name** | Legal or trading name of the startup. | Algolia API |
| **Batch** | The YC funding cycle (e.g., W24, S05). | Algolia API |
| **Industry** | Functional sector of the company. | Algolia API |
| **Company Country** | Country of headquarters (Parsed). | Algolia API |
| **Founded** | The year the company was established. | Profile Page |
| **Team Size** | Number of current employees. | API / Profile Page |
| **Company Status** | Operational status (Active, Acquired, Inactive). | Profile Page |
| **Company Link** | Verifiable YC profile URL. | Generated Slug |

---

## Setup and Execution

### 1. Prerequisite Installation
```bash
pip install -r requirements.txt
```

### 2. Phase 1: Structural Scraping
```bash
python yc_scraper.py
```

### 3. Phase 2: Data Enrichment
```bash
python yc_details_scraper.py
```

---

## Ethical Disclosure
This project was developed for educational purposes to demonstrate advanced data extraction and analysis techniques. The systems built respect the target directory's structure and `robots.txt` constraints. Users are encouraged to maintain ethical scraping standards.
