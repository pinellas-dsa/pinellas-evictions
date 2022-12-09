from evictions.scraper.basepage import BasePage
from evictions.resources.locators import Locators


class HomePage(BasePage):
    """Navigates the home page of CCMSPA."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(
            Locators.CCMPSA_HOMEPAGE_URL
        )  # navigates to the CCMSPA home page
        self.click_all_case_records()

    def click_all_case_records(self) -> None:
        """On the homepage, chooses the option to search all case records"""
        self.click(Locators.ALL_CASE_RECORDS_LINK)
