# Data Collection Pipeline

Implementation of a web scraper that uses Selenium scrapes information from all search results of a search query to the website of British bookseller Waterstones (https://www.waterstones.com/). The scraper sorts the results by language of publication, and returns the information in the form of a csv file and jpg images of all front covers. The project follows a CI/CD workflow using GitHub Actions which automatically pushes a Docker image to my [Docker Hub profile](https://hub.docker.com/u/tuttonluke).

The scraper can be implemented by running the [waterstones_query_headless.py](https://github.com/tuttonluke/aicore_data_collection_pipeline_project/blob/main/project_files/waterstones_query_headless.py) file, or by pulling and running the Docker image found [here](https://hub.docker.com/r/tuttonluke/waterstones_scraper) with the following commands:

1) docker pull tuttonluke/waterstones_scraper
2) docker run -it --rm waterstones_scraper 

# Project Documentation

## Milestone 1: Setting Up a Web Scraper with Selenium
Technologies / Skills:
- Web Scraping (HTML, BeautifulSoup, Selenium, uuid)

I love books and romance languages, so I decided to scrape data of Spanish and Portuguese language authors from the website of popular British bookseller Waterstones. A webscraping class WaterstonesScraper was built using Selenium to drive the Chrome browser. Methods of this class include those to load the page, accept cookies, navigate a search query, and scrape links for all books from the given query.

## Milestone 2: Developing the Selenium Web Scraper
Technologies / Skills:
- Advanced Selenium, Pandas, Os

Further methods for scraping key data from the Waterstones website were developed, including author name, book title, unique identifying number, and front cover images. The scraper also has the functionality to navigate the website's search filtering by language. The data was then systematically saved in a pandas DataFrame and .csv file, as well as downloaded image files of the front covers.

The scraper is run as intended by an instance of the function run_the_scraper, which requires the user to input a list of authors which will be searched:

![run_the_scraper screenshot](project_files\screenshots\run_the_scraper.png?raw=true)

## Milestone 3: Documentation and Testing
Technologies / Skills:
- Abstraction & Encapsulation in OOP
- System, Integration, and Unit Testing
    - unittest
    - pandas.testing
- Project Structure for Software Development

Unit testing of public methods of the QueryWaterstones class was implemented using the python unittest framework. The get_DataFrame_of_language_filtered_query_results method of the WaterstonesScraper class returns scraped data in the form of a pandas DataFrame, so the pandas inbuilt testing framework was also used.

## Milestone 4: Containerising the Waterstones Web Scraper
Technologies / Skills:
- Docker Images & Containers
- Docker Hub

The scraper was refactored for compatibility with containerisation on the Docker platform; for example, implementing an option for running the scraper in headless mode. A docker image which runs the scraper was then built and pushed to [Docker Hub](https://hub.docker.com/repository/docker/tuttonluke/waterstones_scraper). 

## Milestone 5: Setting Up a CI/CD Pipeline for the Docker Image
Technologies / Skills:
- CI/CD Pipelines
- GitHub Actions

A continuous integration / continuous delivery (CI/CD) pipeline was set up using GitHub Actions. The workflow, laid out in the [main.yml](https://github.com/tuttonluke/aicore_data_collection_pipeline_project/blob/main/.github/workflows/main.yml) file, defines steps to check out the repository of the build machine, signs in to Docker Hub using the relevant credentials in the repository secrets, builds the container image, and pushes it to the Docker Hub repository.

CI/CD is an agile DevOps workflow that relies on automation to reduce deployment time and increase software quality through automation of tests, improved system integration, and reduced costs.

