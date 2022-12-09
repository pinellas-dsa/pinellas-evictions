from typing import List
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from evictions.resources.locators import Locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from evictions.scraper.basepage import BasePage
from evictions.scraper.recordpage import RecordPage


class TablePage(BasePage):
    """Navigates a table of eviction records on the CCMSPA web site."""

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.rows = self.count_records_in_table()
        self.rowcount: int = len(self.rows)
        print(self.rowcount)
        self.data_df: pd.DataFrame = self.iterate_rows()

    def count_records_in_table(self):
        self.wait_for_presence(Locators.EVICTION_CASES_CSS)
        list_of_rows = self.driver.find_elements(*Locators.EVICTION_CASES_CSS)
        return list_of_rows

    def iterate_rows(self):
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
