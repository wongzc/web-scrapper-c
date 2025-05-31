import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# Create undetected Chrome driver
options = uc.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
driver = uc.Chrome(options=options)

try:
    url = "https://example.com"  # Change to your target page
    driver.get(url)

    time.sleep(3)  # Wait for page to load

    # Full page screenshot
    driver.save_screenshot("screenshot.png")
    print("Screenshot saved as screenshot.png")

finally:
    driver.quit()
    del driver
