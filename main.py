from scraper.scraper import WebScraper
from config import URL, HEADLESS, SEARCH_LOCATION, MAX_PRICE,MIN_PRICE,BEDROOM, BATHROOM
import time
from selenium.webdriver.common.by import By

def main():
    scraper = WebScraper(headless=HEADLESS)

    try:
        scraper.go_to(URL)
        scraper.type("#filters-panel > div > div.gx-3.gx-sm-4.row > div.col > div > div:nth-child(1) > div > div > input", SEARCH_LOCATION, press_enter=True)
        
        scraper.click("#filters-panel > div > div:nth-child(2) > div > div > div > div:nth-child(1) > button")
        scraper.type('//div[@da-id="price-search-root"]/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/input',MIN_PRICE,by=By.XPATH)
        scraper.type('//div[@da-id="price-search-root"]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/input',MAX_PRICE,by=By.XPATH)
        for i in BEDROOM:
            scraper.click(f'[da-id="bedrooms-{i}"]')
        scraper.scroll_to('[da-id="bathrooms-root"]')
        scraper.click('[da-id="bathrooms-root"]')
        for i in BATHROOM:
            scraper.click(f'[da-id="bathrooms-{i}"]')
        scraper.click('[da-id="search-filter-modal-primary-action"]')
        time.sleep(5)

    finally:
        scraper.quit()

if __name__ == "__main__":
    main()
