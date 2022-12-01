#%%
from pandas.testing import assert_series_equal
from project_files.waterstones_scraper import WaterstonesScraper
from unittest import TestCase
import pandas as pd
import unittest

#%%
class WaterstonesScraperTestCase(TestCase):
    """Test output of the WaterstonesScraper class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Generates the a web scraper object before any tests run.
        """
        cls.test_driver = WaterstonesScraper('Jose Saramago')
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Generates a test driver object for each test.
        """
        self.df = self.test_driver.get_book_data()
        return super().setUp()
    
    # @unittest.skip('Skip')
    def test_IDs(self):
        """Tests expected data in the ID column of the dataframe returned from the
        web driver object.
        """
        expected = pd.Series([9780099573586, 9780099461654, 9781784871789]).astype(str).rename("ID")
        actual = self.df["ID"]
        assert_series_equal(expected, actual)
    
    def test_dtypes(self):
        """Asserts all dtypes are True.
        """
        assert all(self.df.dtypes)




#%%
if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
# %%
