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
        self.list_of_language_page_links = []
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

        # Find language section of the filter bar (not always in the same place!)
        search_filters = self.driver.find_elements(by=By.XPATH, 
            value="//div[@class='filter-header slide-trigger js-filter-trigger']") 
        language_tag = None
        for filter in search_filters:
            if filter.text == "LANGUAGE":
                language_tag = filter
        language_container = self.driver.execute_script("""
        return arguments[0].nextElementSibling""", language_tag)
        
        language_list = language_container.find_elements(by=By.TAG_NAME, value="a")
        for language in language_list:
            language_link = language.get_attribute("href")
            self.list_of_language_page_links.append(language_link)
        # remove link for "less" button if present (only present with more than 5 languages)
        if len(self.list_of_language_page_links) > 6:
            self.list_of_language_page_links.pop()

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
    
    def get_language_name(self):
        language_name = self.driver.find_element(by=By.XPATH, 
            value="/html/body/div[1]/div[3]/div[3]/div[1]/div[1]/div/span")
        return language_name.text
    
    def create_DataFrame_of_page_data(self):
        index = 0
        page_df = pd.DataFrame(columns=["ID", "Timestamp", "Author", "Title", 
            "Language", "Price (£)", "Image_link"])
        for book_link in self.list_of_book_links[:3]:
            self.driver.get(book_link)
            isbn = self.get_ISBN()
            author = self.get_author()
            title = self.get_title()
            price = self.get_price()
            image = self.get_image_link()
            book_dict = {
                        "ID" : isbn,
                        "Timestamp" : time.ctime(), # timestamp of scraping.
                        "Author" : author, 
                        "Title" : title,
                        "Language" : None,
                        "Price (£)" : price,
                        "Image_link" : image
                        }
            df = pd.DataFrame(book_dict, index=[index])
            page_df = pd.concat([page_df, df])
            index += 1
    
        return page_df
    
    def get_DataFrame_of_language_filtered_query_results(self):
        for language_link in self.list_of_language_page_links:
            self.driver.get(language_link)
            try:
                language_name = self.get_language_name()
            except:
                language_name = None
            try:
                self.get_all_book_links_from_page()
            except:
                # only one book
                # get current url
                current_url = self.driver.current_url
                # insert it as the only link in self.list_of_book_links
                self.list_of_book_links = [current_url]
            page_df = self.create_DataFrame_of_page_data()
            page_df["Language"] = language_name
            self.language_filtered_DataFrame = pd.concat([self.language_filtered_DataFrame,
            page_df])
    
    def save_df_as_csv(self):
        if not os.path.exists(f"{self.raw_data_path}/{self.query}"):
            os.mkdir(f"{self.raw_data_path}/{self.query}")
        self.language_filtered_DataFrame.to_csv(f"{self.raw_data_path}/{self.query}/{self.query}.csv")

    
#%%
if __name__ == "__main__":
    author_list = ["jose saramago", "isabel allende", "j r r tolkein", "gabriel garcia marquez"]
    for author in author_list:
        driver = QueryWaterstones()
        driver.load_and_accept_cookies()
        driver.search(author)
        driver.get_language_filter_page_links()
        driver.get_DataFrame_of_language_filtered_query_results()
        driver.save_df_as_csv()



# %%
