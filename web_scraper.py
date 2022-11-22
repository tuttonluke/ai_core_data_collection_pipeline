#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
#%%
class WaterstonesScraper:
    def __init__(self) -> None:
        self.driver = webdriver.Edge()

    def load_and_accept_cookies(self) -> webdriver.Edge:
        """Opens Waterstones website and accepts cookies.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        URL = "https://www.waterstones.com/"
        delay = 10
        self.driver.get(URL)
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-banner-sdk']")))
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value="//button[@id='onetrust-accept-btn-handler']")
            accept_cookies_button.click()
        except TimeoutException:
            print('Loading took too long.')
        
        return self.driver
        
#%%
driver = WaterstonesScraper()
driver.load_and_accept_cookies()
