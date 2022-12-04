#%%
from pandas.testing import assert_series_equal
from project_files.waterstones_query import QueryWaterstones
from unittest import TestCase
import pandas as pd
import unittest
#%%
class WaterstonesQueryTestCase(TestCase):
    """_summary_
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Initiates an instance of the QueryWaterstones class before any 
        tests are run, loads the watersones.com homepage and accepts cookies.
        """
        cls.test_driver = QueryWaterstones()
        cls.test_driver.load_and_accept_cookies()
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_driver.quit_browser()
        return super().tearDownClass()
    
    def setUp(self) -> None:
        """_summary_
        """
        return super().setUp()