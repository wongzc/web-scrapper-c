from scraper.scraper import WebScraper
from config import URL, HEADLESS, SEARCH_LOCATION, MAX_PRICE,MIN_PRICE,BEDROOM, BATHROOM, DATA_COUNT_LIMIT
import time
from selenium.webdriver.common.by import By
import re
import csv

def main():
    scraper = WebScraper(headless=HEADLESS)
    counter = 0 # keep track of number of data count

    with open('listings.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'title', 'address', 'price', 'availability',
            'bedrooms', 'bathrooms', 'size_sqft', 'link'
        ])
        writer.writeheader()
        try:
            # go to page
            scraper.go_to(URL)

            # apply filter, using selenium and Ui, can done part of it through url parameter as well
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
            time.sleep(5) # wait for data load

            # keep looping and getting data until limit
            while counter<DATA_COUNT_LIMIT:
                elements = scraper.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[5]/div[2]/div[1]/div/div[@class="listing-card-banner-root"]')

                # loop the cards in current page
                for ele in elements:
                    counter+=1
                    el=ele.find_element(By.XPATH,".//div/div[1]/div[2]/div")
                    info = el.text
                    data = extract_info(info)  

                    el=ele.find_element(By.XPATH,".//div/div[1]/div[1]/a")
                    link=el.get_attribute('href')
                    data["link"]=link

                    writer.writerow(data)

                    if counter>=DATA_COUNT_LIMIT:
                        break

                # move to next page
                li_list = scraper.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[5]/div[2]/div[1]/ul/li')
                next_page=li_list[-1]
                next_page_link=next_page.find_element(By.XPATH,".//a").get_attribute('href')

                if not next_page_link or next_page_link=='#': # id no more next page
                    break
                scraper.go_to(next_page_link)

        finally:
            scraper.quit()


# to extract and format data
def extract_info(info):
    infos = info.split('\n')

    title = infos[0]
    address = infos[1]

    price_match = re.search(r'\$[\s]*([\d,]+)', infos[2])
    price = price_match.group(1).replace(',', '') if price_match else None

    availability = infos[3]
    bedrooms = infos[4]
    bathrooms = infos[5]

    size_match = re.search(r'([\d,]+)\s*sqft', infos[6])
    size_sqft = size_match.group(1).replace(',', '') if size_match else None

    data=({
        "title": title,
        "address": address,
        "price": price,
        "availability": availability,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "size_sqft": size_sqft
    })
    return data

if __name__ == "__main__":
    main()
