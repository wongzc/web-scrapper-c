from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Setup
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless for test
driver = webdriver.Chrome(service=Service(), options=options)

url = "https://sg.indeed.com/jobs?q=software+engineer&l=Singapore"
driver.get(url)
time.sleep(2)

jobs = []

while len(jobs) < 100:
    listings = driver.find_elements(By.CLASS_NAME, "resultContent")

    for job in listings:
        try:
            title = job.find_element(By.CLASS_NAME, "jobTitle").text
            company = job.find_element(By.CLASS_NAME, "companyName").text
            location = job.find_element(By.CLASS_NAME, "companyLocation").text
            try:
                summary = job.find_element(By.CLASS_NAME, "job-snippet").text
            except:
                summary = ""
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "summary": summary
            })
        except:
            continue

    try:
        next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        next_btn.click()
        time.sleep(2)
    except:
        break  # No more pages

driver.quit()

# Save
df = pd.DataFrame(jobs)
df.to_csv("jobs.csv", index=False)
print("Saved", len(jobs), "jobs.")
