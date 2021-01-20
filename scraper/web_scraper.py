import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Crawler:
    __instance__ = None
     
    def __init__(self):
        """
        Constructor
        """
        if Crawler.__instance__ is None:
            Crawler.__instance__ = self
        else:
            raise Exception("You can not create another Crawler class. Use Crawler.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not Crawler.__instance__:
            Crawler()
        return Crawler.__instance__

    def spider(self, driver_name: str, url: str, drivers_dict: dict):
        driver = self.web_driver(driver_name=driver_name, drivers_dict=drivers_dict)
        html = "<html><head></head><body></body></html>"
        try:
            driver.get(url)
            time.sleep(10)
            html = driver.page_source
        except WebDriverException as exc:
            print(f"Web driver error :::::::: {exc} ")
            pass
        driver.close()
        raw_data = self.raw_body_extractor(html)
        return self.regex(raw_data)

    def web_driver(self, driver_name: str, drivers_dict: dict):
        driver_path = ''
        driver = None
        for key, value in drivers_dict.items():
            if driver_name in key.lower():
                driver_path = value
                break
        if 'chrome' in driver_name.lower():
            options = webdriver.ChromeOptions()
            options.headless = True
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        elif 'firefox' in driver_name.lower():
            options = webdriver.FirefoxOptions()
            options.headless = True
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = webdriver.Firefox(executable_path=driver_path, options=options, log_path='./logs/geckodriver.log')
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def regex(self, raw_text: str)-> str:
        new_body = re.sub('\n', ' ', raw_text)
        return re.sub(' +', ' ', new_body)

    def raw_body_extractor(self, html: str)-> str:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
