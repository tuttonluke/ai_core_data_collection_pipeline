#%%
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import pandas as pd
import requests
import time
#%%
class WaterstonesScraper:

    def __init__(self) -> None:
        try:
            self.driver = webdriver.Edge()
        except:
            print("Query must be a string.")
    
    def load_page(self) -> webdriver.Edge:
        """Loads the waterstones.com homepage.

        Returns
        -------
        webdriver.Edge()
            Edge webdriver on watersones.com homepage.
        """
        URL = "https://www.waterstones.com/"
        self.driver.get(URL)

        return self.driver
    
    def quit_browser(self):
        """Quits the webdriver.
        """
        self.driver.quit()
    
    def accept_cookies(self) -> webdriver.Edge:
        """Accepts cookies on entry to the waterstones website.

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, 
                "//*[@id='onetrust-banner-sdk']")))
            accept_cookies_button = self.driver.find_element(by=By.XPATH, 
                value="//button[@id='onetrust-accept-btn-handler']")
            accept_cookies_button.click()
        except TimeoutException:
            print('Loading took too long.')
        
        return self.driver
    
    def load_and_accept_cookies(self) -> webdriver.Edge:
        """Loads the page and accepts cookies. 

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        self.load_page()
        self.accept_cookies()

        return self.driver
    
    def scroll_to_bottom(self):
        """Scrolls to the bottom of the current page by executing JavaScript command.

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        self.driver.execute_script("document.getElementById('footer').scrollIntoView();")

        return self.driver
    
    def click_show_more(self):
        """Clicks the show more button in search result page.

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        show_more = self.driver.find_element(by=By.XPATH, 
            value="//button[@class='button button-teal']")
        if show_more.is_displayed():
            show_more.click()

        return self.driver
    
    def display_all_results(self):
        """Scrolls down to load all pages of results of a query.

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        number_of_pages = self.driver.find_element(by=By.XPATH, 
            value="/html/body/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/span[2]")
        number_of_pages_text = number_of_pages.text
        number_of_pages_text = number_of_pages_text.replace('of', '')
        number_of_pages_integer = int(number_of_pages_text)
        print(f"Number of pages is {number_of_pages_integer}.")
        page_counter = 0
        while page_counter <= number_of_pages_integer:
            self.scroll_to_bottom()
            self.click_show_more()
            time.sleep(2) # wait for next page of results to load
            page_counter += 1
        
        return self.driver
    
    def get_author(self) -> str:
        """Srapes the author's name.

        Returns
        -------
        str
            Name of the author.
        """
        author = self.driver.find_element(by=By.XPATH, 
            value="//span[@itemprop='author']").text

        return author

    def get_title(self) -> str:
        """Srapes the book title.

        Returns
        -------
        str
            Title of the book.
        """
        title = self.driver.find_element(by=By.XPATH, 
            value="//span[@class='book-title']").text

        return title

    def get_ISBN(self) -> int:
        """Scrapes ISBN (International Standard Book Number), a unique product identifier
        used by publishers and booksellers. The ISBN identifies the specific title,
        edition, and format.

        Returns
        -------
        int
            ISBN number.
        """
        isbn = self.driver.current_url[-13:]

        return int(isbn)
    
    def get_price(self) -> float:
        """Scrapes price in GBP.

        Returns
        -------
        float
            Item price.
        """
        price = self.driver.find_element(by=By.XPATH,
            value="//b[@itemprop='price']").text
        price = price.strip('£')

        return float(price)
    
    def get_image_link(self) -> str:
        """Scrapes links for book images.

        Returns
        -------
        str
            Source of image link.
        """
        img = self.driver.find_element(by=By.XPATH,
            value="//img[@itemprop='image']")
        img_src = img.get_attribute("src")

        return img_src
    
    def download_img(self, img_url: str, file_path: str):
        """Downloads image to current directory.

        Parameters
        ----------
        img_url : str
            URL of image to be downnloaded.
        file_path : str
            File path of location where the image is to be saved.
        """
        img_data = requests.get(img_url).content
        with open(file_path, "wb") as handler:
            handler.write(img_data)
    
#%%
if __name__ == "__main__":
    driver = WaterstonesScraper()

    try:
        driver.load_and_accept_cookies()
        driver.scroll_to_bottom()
    
    except Exception as e:
        print(e)
        driver.quit_browser()
    

