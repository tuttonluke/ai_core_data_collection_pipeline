#%%
from project_files.waterstones_scraper import WaterstonesScraper
import unittest
import pandas as pd
from pandas.testing import assert_series_equal

#%%
class WaterstonesScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_driver = WaterstonesScraper('Jose Saramago')
        return super().setUp()
    
    def test_IDs(self):
        expected = pd.Series([9780099573586, 9780099461654, 9781784871789]).astype(str).rename("ID")
        actual = self.test_driver.get_book_data()["ID"]
        assert_series_equal(expected, actual)
    



#%%
unittest.main(argv=[''], exit=False)
# %%
