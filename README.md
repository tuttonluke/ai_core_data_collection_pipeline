# Data Collection Pipeline

(One sentence description)

(How to implement)

(Add screenshots)

# Project Documentation

(brief description of the project)

## Milestone 1: Setting Up a Web Scraper with Selenium
Technologies / Skills:
- Web Scraping (HTML, BeautifulSoup, Selenium, uuid)

I love books and romance languages, so I decided to scrape data of Spanish and Portuguese language authors from the website of popular British bookseller Waterstones. A webscraping class WaterstonesScraper was built using Selenium to drive the Edge browser. Methods of this class include those to load the page, accept cookies, navigate a search query, and scrape links for all books from the given query.

## Milestone 2: Developing the Selenium Web Scraper
Technologies / Skills:
- Advanced Selenium, Pandas, Os

Further methods for scraping key data from the Waterstones website were developed, including author name, book title, unique identifying number, and front cover images. The data was then systematically saved in a pandas DataFrame and .csv file, as well as downloaded image files of the front covers.

## Milestone 3: Documentation and Testing
Technologies / Skills:
- Abstraction & Encapsulation in OOP
- System, Integration, and Unit Testing
    - unittest
    - pandas.testing
- Project Structure for Software Development

Unit testing of public methods of the QueryWaterstones class was implemented using the python unittest framework. The get_DataFrame_of_language_filtered_query_results method of the WaterstonesScraper class returns scraped data in the form of a pandas DataFrame, so the pandas inbuilt testing framework was also used.