from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import random
import undetected_chromedriver as uc

def scrape_indeed_jobs(max_jobs=100):
    options = Options()
    # options.add_argument("--headless")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(), options=options)
    url = "https://sg.indeed.com/jobs?q=software+engineer&l=Singapore"
    driver.get(url)
    time.sleep(2)

    jobs = []

    while len(jobs) < max_jobs:
        listings = driver.find_elements(By.CLASS_NAME, "resultContent")

        for job in listings:
            try:
                title = job.find_element(By.CLASS_NAME, "jobTitle").text
                company = job.find_element(By.CLASS_NAME, "companyName").text
                location = job.find_element(By.CLASS_NAME, "companyLocation").text
                summary = job.find_element(By.CLASS_NAME, "job-snippet").text
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "summary": summary.strip().replace("\n", " ")
                })
            except:
                continue

        try:
            next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
            next_btn.click()
            time.sleep(random.uniform(1.5, 3.0))
        except:
            break

    driver.quit()
    return jobs

if __name__ == "__main__":
    data = scrape_indeed_jobs()
    df = pd.DataFrame(data)
    df.to_csv("jobs.csv", index=False)
    print(f"Saved {len(df)} job listings to jobs.csv.")