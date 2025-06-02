# Web Scraping Take-Home Test Report
## Objective
Build a robust web scraper that:
- Extract structured listing data
- Handle UI filters and pagination
- Output at least 100 records in CSV format

## Tools & Technologies
- Language: Python
- Framework: Selenium + undetected_chromedriver (bypass bot detection)
- Output: CSV file

## Features Implemented
1. Dynamic Filtering:
 - Location, min/max price, bedrooms, bathrooms based on config.py
 - Uses direct input and interactive click simulation through selenium

2. Pagination Handling:
 - Automatically navigate through pages using the "Next" link that get from the UI

3. Data Fields Extracted:
 - Title, address, price, availability, bedrooms, bathrooms, size, detail page link

4. Extraction Limit: Controlled via DATA_COUNT_LIMIT in config.py

## Code Structure
1. main.py:
 - Controls the scraping logic and CSV export

2. scraper.py:
- Modular class (WebScraper) for interaction with the browser (type, click, scroll ...)

## Output
listings.csv with structured data, each row representing one rental listing

## Error Handling & Cleanup
Uses try-finally to ensure browser closes cleanly after scraping