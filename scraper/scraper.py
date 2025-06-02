from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


class WebScraper:
    """ utility function for driver"""
    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def go_to(self, url):
        self.driver.get(url)

    def click(self, selector, by=By.CSS_SELECTOR):
        elem = self.wait.until(EC.element_to_be_clickable((by, selector)))
        elem.click()

    def type(self, selector, text, by=By.CSS_SELECTOR, press_enter=False):
        elem = self.wait.until(EC.presence_of_element_located((by, selector)))
        elem.clear()
        elem.send_keys(text)
        if press_enter:
            elem.send_keys(Keys.ENTER)

    def get_elements(self, selector, by=By.CSS_SELECTOR):
        return self.driver.find_elements(by, selector)

    def get_texts(self, selector, by=By.CSS_SELECTOR):
        return [el.text for el in self.get_elements(selector, by)]

    def scroll_to(self, selector, by=By.CSS_SELECTOR):
        elem = self.driver.find_element(by, selector)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    
    def quit(self):
        self.driver.quit()
