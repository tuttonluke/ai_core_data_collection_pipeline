#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
#%%
class WaterstonesScraper:
    """_summary_
    """
    def __init__(self, query) -> None:
        self.driver = webdriver.Chrome()
        self.query = query
        self.link_list = []
        self.book_df = pd.DataFrame(columns=["Author", "Title"])

    def load_and_accept_cookies(self) -> webdriver.Chrome:
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
    
    def search(self) -> webdriver.Chrome:
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
        search_bar = self.driver.find_element(by=By.XPATH, value="//input[@class='input input-search']")
        search_bar.click()
        try:
            search_bar.send_keys(self.query)
            search_bar.send_keys(Keys.RETURN)
        except:
            print('Invalid query input.')

        return self.driver
    
    def scroll_to_bottom(self) -> webdriver.Chrome:
        """Scrolls to the bottom of the current page.

        Returns
        -------
        webdriver.Edge
            This driver is already in the Waterstones webpage.
        """
        self.driver.execute_script("document.getElementById('footer').scrollIntoView();")

        return self.driver
    
    def click_show_more(self) -> webdriver.Chrome:
        """Clicks the show more button in search result page.

        Returns
        -------
        webdriver.Chrome
            This driver is already in the Waterstones webpage.
        """
        show_more = self.driver.find_element(by=By.XPATH, value="//button[@class='button button-teal']")
        if show_more.is_displayed():
            show_more.click()
        return self.driver
    
    def display_all_results(self) -> webdriver.Chrome:
        """Loads all pages from a query result.

        Returns
        -------
        webdriver.Chrome
            This driver is already in the Waterstones webpage.
        """
        span = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/span[2]")
        text = span.text
        text = text.replace('of', '')
        no_pages = int(text)
        print(f"No. pages is {no_pages}.")
        counter = 0
        while counter <= no_pages:
            self.scroll_to_bottom()
            self.click_show_more()
            time.sleep(3) # wait for next page of results to load
            counter += 1
        return self.driver
    

    def get_all_book_links(self) -> webdriver.Chrome:
        """Gathers all links for books in a search query in to class attribute 
        link_list.

        Returns
        -------
        webdriver.Chrome
            This driver is already in the Waterstones webpage.
        """
        driver.load_and_accept_cookies()
        driver.search()
        driver.display_all_results()
        time.sleep(2)
        book_container = self.driver.find_element(by=By.XPATH, value="//div[@class='search-results-list']")
        book_list = book_container.find_elements(by=By.XPATH, value="./div")
        for book in book_list:
            a_tag = book.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.link_list.append(link)

        return self.driver
    
    def get_author(self):
        """Srapes the author's name.

        Returns
        -------
        str
            Name of the author.
        """
        author = self.driver.find_element(by=By.XPATH, value="//span[@itemprop='author']").text
        return author

    def get_title(self):
        """Srapes the book title.

        Returns
        -------
        str
            Title of the book.
        """
        title = self.driver.find_element(by=By.XPATH, value="//span[@class='book-title']").text
        return title
    
    def get_book_data(self):
        for book_link in self.link_list:
            self.driver.get(book_link)
            author = self.get_author()
            title = self.get_title()
            
            book_dict = {"Author" : author, 
                        "Title" : title
                        }
            self.book_df = self.book_df.append(book_dict, ignore_index=True)
        return book_df
#%%

if __name__ == "__main__":
    driver = WaterstonesScraper("Jose Saramago")
    # driver = WaterstonesScraper("gabriel garcia marquez")
    # driver = WaterstonesScraper("isabel allende")
    driver.get_all_book_links()
    print(len(driver.link_list))
    df = driver.get_book_data()

    # driver.quit()
#%%

book_df = pd.DataFrame(columns=["Author", "Title"])
book_dict = {"Author" : "Jose Saramago", 
                        "Title" : "Blindness"
                        }

