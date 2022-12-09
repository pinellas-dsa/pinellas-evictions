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

    def click_all_case_records(self):
        self.click(Locators.ALL_CASE_RECORDS_LINK)

    def select_search_by_date(self):
        radio_list = self.driver.find_element(
            *Locators.SEARCH_BY_RADIO_BUTTONS_ID
        )

        for rbutton in radio_list:
            rbutton_t = rbutton.get_attribute("id")
            if rbutton_t == "DateFiled":
                rbutton.click()
                break
