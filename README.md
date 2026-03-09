# Y Combinator Startup Ecosystem: A Comprehensive Data Analysis

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
The data highlights a significant geographic centralisation within the United States. Despite the rise of global entrepreneurship, the US remains the primary epicenter for venture-backed talent. Notably, **San Francisco accounts for approximately 43% of all companies** in the dataset, underscoring the enduring importance of proximity to capital and specialized talent pools.

![Geographical Concentration Map](https://github.com/user-attachments/assets/343d4546-5c6e-4c96-9cf9-b17d3c55d760)

### 2. Strategic Shift to B2B and SaaS
Analysis of industry trends over time reveals a maturation of the startup ecosystem. Early YC batches featured a higher proportion of consumer-facing applications. However, modern cohorts show a clear pivot toward **B2B (Business-to-Business) and SaaS (Software as a Service)** models. This shift indicates a move toward high-retention enterprise solutions over more volatile consumer markets.

![Industry Shift Trends](https://github.com/user-attachments/assets/ede107f5-25e7-4447-8793-35cda03903d6)

### 3. Sustainability of Remote Operations
While the 2021 pandemic triggered a massive spike in remote-first startups, the trend has established a new baseline rather than reverting to pre-2020 levels. Currently, **roughly 30% of new startups** choose remote operations, suggesting that distributed teams have evolved into a viable, long-term structural strategy for early-stage companies.

![Remote vs Office Trends](https://github.com/user-attachments/assets/850d0ba0-bb0f-4ee2-ac8d-1451e8d7beac)

### 4. Long-term Survival and Cohort Analysis
Survival metrics require a multi-year lens to reach statistical significance. While recent batches (2023-2024) show high survival rates (>90%), historical data from 2010-2015 shows that **long-term survival stabilizes around 70%**. This 10-year window is the typical horizon for acquisition, IPO, or market exit.

![Survival and Acquisition Cohorts](https://github.com/user-attachments/assets/922b151a-4719-4e67-8a53-36be55b48138)

### 5. Vertical Growth of Artificial Intelligence
Artificial Intelligence has transitioned from a niche category to a foundational requirement. Since late 2022, the growth curve for AI-focused startups has outpaced all other sectors in YC history. AI is increasingly integrated as a core feature of the tech stack across all industries rather than being treated as a standalone vertical.

![YoY Growth by Technology](https://github.com/user-attachments/assets/9b78b883-d8e7-4e73-8f64-1e2e55dffd33)

### 6. Lean Team Efficiency
The headcount required to launch and scale a startup is decreasing. Historically, team sizes were larger at the early stages; however, modern startups are frequently launched by **lean teams of 2 to 3 founders**. The proliferation of AI-assisted development tools and automated infrastructure is enabling "high-output, low-headcount" efficiency.

![Average Team Size Evolution](https://github.com/user-attachments/assets/4bdb9ca7-4ffe-44c7-a86f-33142c0ed4bb)

### 7. Sector-Specific Risk Assessment
The data reveals clear risk/reward profiles across sectors. High-volatility sectors like **Social Media show failure rates exceeding 50%**, whereas highly regulated or technical sectors such as **Healthcare and Biotech show higher rates of public exit**. This suggests that while barriers to entry are higher in specialized sectors, their long-term stability is significantly greater.

![Sector Risk/Reward Scatter Plot](https://github.com/user-attachments/assets/a427642e-660e-48c4-bba1-40e04e0311f5)

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
