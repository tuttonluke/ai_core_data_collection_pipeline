#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
#%%
class Scraper:
    def __init__(self) -> None:
        pass

    def load_and_accept_cookies(self) -> webdriver.Edge:
        """Opens Waterstones website and accepts cookies.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        driver = webdriver.Edge()
        URL = "https://www.waterstones.com/"
        driver.get(URL)
        accept_cookies_button = driver.find_element(by=By.XPATH, value="//button[@id='onetrust-accept-btn-handler']")
        time.sleep(2) # wait 2 seconds so the website doesn't think you're a bot
        accept_cookies_button.click()

        return driver
#%%
driver = Scraper()
driver.load_and_accept_cookies()
