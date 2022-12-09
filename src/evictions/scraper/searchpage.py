from selenium import webdriver
from selenium.webdriver.support.select import Select
from evictions.scraper.basepage import BasePage
from evictions.resources.locators import Locators


class SearchPage(BasePage):
    """Navigates the search page of CCMSPA, in which the user selects search parameters including:

    - start date
    - end date
    - case type
    """

    def __init__(
        self,
        driver: webdriver.Chrome,
        start_date: str,
        end_date: str,
        case_type: str,
    ):
        super().__init__(driver)
        self.select_search_by_date()
        self.select_start_end_dates(start_date, end_date)
        self.select_case_type(case_type)
        self.click_search_submit()

    def select_search_by_date(self):
        radio_list = self.driver.find_elements(
            *Locators.SEARCH_BY_RADIO_BUTTONS_ID
        )

        for rbutton in radio_list:
            rbutton_t = rbutton.get_attribute("id")
            if (
                rbutton_t == Locators.DATE_FILED_BUTTON_ID
            ):  # value will be "DateFiled"
                rbutton.click()
                break

    def select_start_end_dates(self, start_date: str, end_date: str):
        """Finds and fills in the start and end date fields on the 'All Case Records'
        search page on the CCMSPA site.

        Args:
            start_date (str): first day to search records
            end_date (str): last day to search records
        """
        self.enter_text(Locators.DATE_ON_OR_AFTER_ID, start_date)
        self.enter_text(Locators.DATE_ON_OR_BEFORE_ID, end_date)

    def select_case_type(self, case_type: str):
        """_summary_

        Args:
            case_type (str): _description_
        """
        dropdown = Select(
            self.driver.find_element(*Locators.CASE_TYPE_DROPDOWN_ID)
        )
        dropdown.select_by_visible_text(case_type)

    def click_search_submit(self):
        self.click(Locators.SUBMIT_BUTTON_ID)
