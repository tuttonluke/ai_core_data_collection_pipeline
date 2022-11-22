#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
#%%
class WaterstonesScraper:
    """_summary_
    """
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
    
    def search(self, query) -> webdriver.Edge:
        search_bar = self.driver.find_element(by=By.XPATH, value="//input[@class='input input-search']")
        search_bar.click()
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.RETURN)

        return self.driver
        
#%%

if __name__ == "__main__":
    driver = WaterstonesScraper()
    driver.load_and_accept_cookies()
    driver.search("José Saramago")
