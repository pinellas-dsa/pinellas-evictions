from typing import List
import pandas as pd
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from evictions.resources.locators import Locators
from evictions.scraper.basepage import BasePage
from evictions.scraper.recordpage import RecordPage


class TablePage(BasePage):
    """Navigates a table of eviction records on the CCMSPA web site."""

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.rows = self.get_records_in_table()
        self.rowcount: int = len(self.rows)
        print(self.rowcount)
        self.data_df: pd.DataFrame = self.iterate_rows()

    def get_records_in_table(self) -> List(WebElement):
        """Finds a returns a list of WebElements, where each WebElement
        represents one row in the table of eviction cases.

        Returns:
            list_of_rows: The list of eviction cases in the web table
        """
        self.wait_for_presence(Locators.EVICTION_CASES_CSS)
        list_of_rows = self.driver.find_elements(*Locators.EVICTION_CASES_CSS)
        return list_of_rows

    def iterate_rows(self) -> pd.DataFrame:
        """Loops through the rows of the table of eviction cases.
        For each row, clicks on it and then creates a RecordPage to
        slurp the data out of it.

        Returns:
            month_of_data_df: DataFrame containing one month of eviction data.
        """
        eviction_list = []
        for index in range(self.rowcount):
            row = self.driver.find_elements(*Locators.EVICTION_CASES_CSS)[
                index
            ]
            row.click()
            # get the data for the current eviction record
            record_data = RecordPage(self.driver).record_data
            # convert the record to a one-row DataFrame
            record_data_df = pd.DataFrame.from_records(record_data)
            # add the data to a list of records
            eviction_list.append(record_data_df)
            self.driver.back()
        month_of_data_df = pd.concat(eviction_list)
        return month_of_data_df
