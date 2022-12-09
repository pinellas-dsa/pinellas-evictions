from typing import Tuple
from selenium.webdriver.common.by import By


class Locators:
    """Contains attributes used to locate objects in the DOM for various pages used in the scraper.
    Note that most locators are stored as a tuple and will require unpacking when used.

    For example: cdriver.find_element(*Locators.ALL_CASE_RECORDS_LINK).click()"""

    # --- Home Page Locators ---
    CCMPSA_HOMEPAGE_URL: str = (
        "https://ccmspa.pinellascounty.org/PublicAccess/"
    )
    # --- Search Page Locators ---
    SEARCH_BY_RADIO_BUTTONS_ID: Tuple[By, str] = (By.NAME, "SearchBy")
    ALL_CASE_RECORDS_LINK: Tuple[By, str] = (
        By.LINK_TEXT,
        "All Case Records Search",
    )
    DATE_FILED_BUTTON_ID: str = "DateFiled"
    DATE_ON_OR_AFTER_ID: Tuple[By, str] = (By.ID, "DateFiledOnAfter")
    DATE_ON_OR_BEFORE_ID: Tuple[By, str] = (By.ID, "DateFiledOnBefore")
    SUBMIT_BUTTON_ID: Tuple[By, str] = (By.ID, "SearchSubmit")
    CASE_TYPE_DROPDOWN_ID: Tuple[By, str] = (By.ID, "selCaseTypeGroups")
    # --- Table Page Locators
    EVICTION_CASES_CSS: Tuple[By, str] = (
        By.CSS_SELECTOR,
        "a[href*='CaseID']",
    )
    # --- Record Page Locators
    CASE_DETAIL_CLASS = (By.CLASS_NAME, "ssCaseDetailCaseNbr")
    RECORD_ROW_XPATH = (By.XPATH, "//table/tbody/tr")
