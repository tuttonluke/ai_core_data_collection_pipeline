#%%
from waterstones_scraper_class import WaterstonesScraper
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
class QueryWaterstones(WaterstonesScraper):
    def __init__(self) -> None:
        
        super().__init__()
        self.query = None
        self.dict_of_languages = {}
        self.list_of_book_links = []
        self.language_filtered_DataFrame = pd.DataFrame(columns=["ID", "Timestamp", "Author", "Title", 
            "Language", "Price (£)", "Image_link"])
    
    def search(self, query) -> webdriver.Edge:
        """Searches given query in waterstones website searchbar.

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        self.query = query.replace(" ", "_").lower()
        search_bar = self.driver.find_element(by=By.XPATH, 
            value="//input[@class='input input-search']")
        search_bar.click()
        try:
            search_bar.send_keys(self.query.replace("_", " "))
            search_bar.send_keys(Keys.RETURN)
        except:
            print("Invalid query input.")

        return self.driver
    
    def get_language_filter_page_links(self):

        # click more button in language filter section
        language_more_button_xpath = "/html/body/div[1]/div[3]/div[3]/div[1]/div[2]/div[7]/div[2]/div/a"
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, 
            language_more_button_xpath))).click()
        # populate self.dict_of_languages
        language_container = self.driver.find_element(by=By.XPATH, 
            value="/html/body/div[1]/div[3]/div[3]/div[1]/div[2]/div[7]/div[2]/div")
        language_list = language_container.find_elements(by=By.TAG_NAME, value="a")
        for language in language_list:
            language_name = language.text
            language_link = language.get_attribute("href")
            self.dict_of_languages[language_name] = language_link
        # remove information concerned with the 'less' button
        self.dict_of_languages.pop("Less")
        
        return self.driver

    def get_all_book_links_from_page(self):
        """Populates self.list_of_book_links with all the links to books on the
        current page.

        Returns
        -------
        webdriver.Edge
            Edge webdriver.
        """
        self.list_of_book_links = []
        book_container = self.driver.find_element(by=By.XPATH, 
            value="//div[@class='search-results-list']")
        book_list = book_container.find_elements(by=By.XPATH, value="./div")
        for book in book_list:
            a_tag = book.find_element(by=By.TAG_NAME, value="a")
            link = a_tag.get_attribute("href")
            self.list_of_book_links.append(link)
        print(f"Number of items is {len(self.list_of_book_links)}.")

        return self.driver
    
    def get_DataFrame_of_language_filtered_query_results(self):
        for language in self.dict_of_languages:
            self.driver.get(self.dict_of_languages[language])
            self.display_all_results()
            self.get_all_book_links_from_page()
            page_df = self.create_DataFrame_of_page_data()
            page_df["Language"] = language
            self.language_filtered_DataFrame = pd.concat([self.language_filtered_DataFrame,
            page_df])
    
#%%
if __name__ == "__main__":
    driver = QueryWaterstones()
    driver.load_and_accept_cookies()
    driver.search("jose saramago")
    driver.get_language_filter_page_links()
    driver.get_DataFrame_of_language_filtered_query_results()

#%%

    # driver.get_all_book_links_from_page()
    # df = driver.create_DataFrame_of_page_data()