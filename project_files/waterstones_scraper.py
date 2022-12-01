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
    """This class generates a web scraper to scrape key data from the
    popular bookseller Waterstone's website, based on a query entered
    by the user. 
    """
    def __init__(self, query) -> None:
        """Initialises the class.

        Parameters
        ----------
        query : str
            Query to search in the Waterstones website. Data will then
            be scraped from all search results.
        
        Attributes
        ----------
        driver : webdriver.Edge
                 Instance of the Edge webdriver.
        __query : str
                  Query to be searched.
        __raw_data_path : str
                          File path in which to save raw data.
        link_list : list
                    List of links of query results.
        language_link_list : list
                            List of links of language-filtered pages of query results.
        book_df : DataFrame
                  Dataframe of query result data. 
        """
        try:
            self.driver = webdriver.Edge()
            self.__query = query.replace(' ', '_').lower()
            self.__raw_data_path = r"C:\Users\tutto\OneDrive\Documents\Documents\AiCore\Projects\ai_core_data_collection_pipeline\project_files\raw_data"
            self.link_list = []
            self.language_link_list = []
            self.book_df = pd.DataFrame(columns=["ID", "Timestamp", "Author", "Title", 
                "Price (£)", "Image_link"])
        except:
            print("Query must be a string.")

    def __load_and_accept_cookies(self) -> webdriver.Edge:
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
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, 
                "//*[@id='onetrust-banner-sdk']")))
            accept_cookies_button = self.driver.find_element(by=By.XPATH, 
                value="//button[@id='onetrust-accept-btn-handler']")
            accept_cookies_button.click()
        except TimeoutException:
            print('Loading took too long.')
        
        return self.driver
    
    def quit_browser(self):
        """Quits the browser.
        """
        self.driver.quit()
    
    def __search(self) -> webdriver.Edge:
        """Searches given query in website searchbar.

        Parameters
        ----------
        query : str, int, float
            Query to be searched.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.

        """
        search_bar = self.driver.find_element(by=By.XPATH, 
            value="//input[@class='input input-search']")
        search_bar.click()
        try:
            search_bar.send_keys(self.__query.replace('_', ' '))
            search_bar.send_keys(Keys.RETURN)
        except:
            print('Invalid query input.')

        return self.driver
    
    def __scroll_to_bottom(self) -> webdriver.Edge:
        """Scrolls to the bottom of the current page.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        self.driver.execute_script("document.getElementById('footer').scrollIntoView();")

        return self.driver
    
    def __click_show_more(self) -> webdriver.Edge:
        """Clicks the show more button in search result page.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        show_more = self.driver.find_element(by=By.XPATH, 
            value="//button[@class='button button-teal']")
        if show_more.is_displayed():
            show_more.click()

        return self.driver
    
    def __display_all_results(self) -> webdriver.Edge:
        """Loads all pages from a query result.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        span = self.driver.find_element(by=By.XPATH, 
            value="/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/span[2]")
        text = span.text
        text = text.replace('of', '')
        no_pages = int(text)
        print(f"Number of pages is {no_pages}.")
        counter = 0
        while counter <= no_pages:
            self.__scroll_to_bottom()
            self.__click_show_more()
            time.sleep(2) # wait for next page of results to load
            counter += 1

        return self.driver
    
    def __get_all_book_links(self) -> webdriver.Edge:
        """Gathers all links for books in a search query in to class attribute 
        link_list.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        self.__load_and_accept_cookies()
        self.__search()
        self.__display_all_results()
        time.sleep(2)
        book_container = self.driver.find_element(by=By.XPATH, 
            value="//div[@class='search-results-list']")
        book_list = book_container.find_elements(by=By.XPATH, value="./div")
        for book in book_list:
            a_tag = book.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.link_list.append(link)
        print(f'Number of items is {len(self.link_list)}.')

        return self.driver
    
    def __get_author(self) -> str:
        """Srapes the author's name.

        Returns
        -------
        str
            Name of the author.
        """
        author = self.driver.find_element(by=By.XPATH, 
            value="//span[@itemprop='author']").text

        return author

    def __get_title(self) -> str:
        """Srapes the book title.

        Returns
        -------
        str
            Title of the book.
        """
        title = self.driver.find_element(by=By.XPATH, 
            value="//span[@class='book-title']").text

        return title

    def __get_ISBN(self) -> int:
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
    
    def __get_price(self) -> float:
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
    
    def __get_image_link(self) -> str:
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
    
    def __download_img(self, img_url: str, file_path: str):
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
    
    def __save_df_as_csv(self):
        """Saves data in a .csv file under the name of the author, creating a new file if one does
        not already exist.
        """
        if not os.path.exists(f"{self.__raw_data_path}/{self.__query}"):
            os.mkdir(f"{self.__raw_data_path}/{self.__query}")
        self.book_df.to_csv(f"{self.__raw_data_path}/{self.__query}/{self.__query}.csv")

    def get_all_book_data(self) -> pd.DataFrame:
        """Calls methods to scrape ISBN ID, author's name, book title, price in GBP,
        and book image source link. Stores data in DataFrame. 

        Returns
        -------
        pd.DataFrame
            DataFrame of scraped data.
        """
        self.__get_all_book_links()
        index = 0
        for book_link in self.link_list[:3]:
            self.driver.get(book_link)
            isbn = self.__get_ISBN()
            author = self.__get_author()
            title = self.__get_title()
            price = self.__get_price()
            image = self.__get_image_link()
            book_dict = {
                        "ID" : isbn,
                        "Timestamp" : time.ctime(), # timestamp of scraping.
                        "Author" : author, 
                        "Title" : title,
                        "Price (£)" : price,
                        "Image_link" : image
                        }
            df = pd.DataFrame(book_dict, index=[index])
            self.book_df = pd.concat([self.book_df, df])
            index += 1
            #self.book_df = self.book_df.append(book_dict, ignore_index=True)
        self.book_df = self.book_df.astype(str)

        return self.book_df
    
    def __get_language_page_links(self):
        """Loads web driver and search query, before gathering all links to pages with language filters

        Returns
        -------
        list
            List of links for language-filtered results of the query.
        """
        self.__load_and_accept_cookies()
        self.__search()
        language_container = self.driver.find_element(by=By.XPATH, 
            value="/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[7]/div[2]/div")
        language_list = language_container.find_elements(by=By.TAG_NAME, value="a")
        for language in language_list:
            language_link = language.get_attribute("href")
            self.language_link_list.append(language_link)
        self.language_link_list.pop()

        return self.driver

    def get_book_data_with_language_filter(self):
        
        language_link_list = self.__get_language_page_links()
        for language_page in language_link_list:
            self.__display_all_results()



    def save_book_data(self):
        """Save DataFrame in csv file and save images in images folder. 
        """
        self.__save_df_as_csv()
        os.mkdir(f"{self.__raw_data_path}/{self.__query}/images")
        for img_url in self.book_df["Image_link"]:
            isbn = img_url[-17:-4]
            self.__download_img(img_url, f"{self.__raw_data_path}/{self.__query}/images/{isbn}.jpg")

    

#%%
if __name__ == "__main__":
    driver = WaterstonesScraper("jose saramago")
    # driver = WaterstonesScraper("gabriel garcia marquez")
    # driver = WaterstonesScraper("isabel allende")
    # driver = WaterstonesScraper(2)

    try:
        # df = driver.get_all_book_data()
        # driver.save_book_data()
        language_list = driver.get_book_data_with_language_filter()
    except Exception as e:
        print(e)
        driver.quit_browser()
        
#%%