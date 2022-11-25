#%%
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import os
import requests
#%%
class WaterstonesScraper:
    """_summary_
    """
    def __init__(self, query) -> None:
        self.driver = webdriver.Chrome()
        self.__query = query.replace(' ', '_').lower()
        self.link_list = []
        self.book_df = pd.DataFrame(columns=["ID", "Timestamp", "Author", "Title", 
            "Price (£)", "Image_link"])

    def __load_and_accept_cookies(self) -> webdriver.Chrome:
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
    
    def __search(self) -> webdriver.Chrome:
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
            search_bar.send_keys(self.__query)
            search_bar.send_keys(Keys.RETURN)
        except:
            print('Invalid query input.')

        return self.driver
    
    def __scroll_to_bottom(self) -> webdriver.Chrome:
        """Scrolls to the bottom of the current page.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        self.driver.execute_script("document.getElementById('footer').scrollIntoView();")

        return self.driver
    
    def __click_show_more(self) -> webdriver.Chrome:
        """Clicks the show more button in search result page.

        Returns
        -------
        webdriver.Chrome
            This driver is already in the Waterstones webpage.
        """
        show_more = self.driver.find_element(by=By.XPATH, 
            value="//button[@class='button button-teal']")
        if show_more.is_displayed():
            show_more.click()

        return self.driver
    
    def __display_all_results(self) -> webdriver.Chrome:
        """Loads all pages from a query result.

        Returns
        -------
        webdriver.Chrome
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
            time.sleep(3) # wait for next page of results to load
            counter += 1

        return self.driver
    
    def __get_all_book_links(self) -> webdriver.Chrome:
        """Gathers all links for books in a search query in to class attribute 
        link_list.

        Returns
        -------
        webdriver.Chrome
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
    
    def __download_img(self, img_url, file_path):
        """Downloads image.

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
        """Saves data in a .csv file under the name of the author, if the file does
        not already exist.
        """
        if not os.path.exists(f"raw_data/{self.__query}"):
            os.mkdir(f"raw_data/{self.__query}")
        self.book_df.to_csv(f"raw_data/{self.__query}/{self.__query}.csv")

    def get_book_data(self) -> pd.DataFrame:
        """Calls methods to scrape ISBN ID, author's name, book title, price in GBP,
        and book image source link. Stores data in DataFrame. 

        Returns
        -------
        pd.DataFrame
            DataFrame of scraped data.
        """
        self.__get_all_book_links()
        for book_link in self.link_list:
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
            self.book_df = self.book_df.append(book_dict, ignore_index=True)

        return self.book_df

    def save_book_data(self):
        """Save DataFrame in csv file and save images in images folder. 
        """
        self.__save_df_as_csv()
        os.mkdir(f"raw_data/{self.__query}/images")
        for img_url in self.book_df["Image_link"]:
            isbn = img_url[-17:-4]
            self.__download_img(img_url, f"raw_data/{self.__query}/images/{isbn}.jpg")

    

#%%
if __name__ == "__main__":
    driver = WaterstonesScraper("jose saramago")
    # driver = WaterstonesScraper("gabriel garcia marquez")
    # driver = WaterstonesScraper("isabel allende")
    df = driver.get_book_data()
    driver.save_book_data()
#%%