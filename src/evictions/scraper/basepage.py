from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class BasePage:
    """This class is the parent class for all the pages in the scraper. It
    contains all common elements and functionalities available to all pages."""

    def __init__(self, driver: webdriver.Chrome):
        """Initializes the page.

        Args:
            driver (webdriver.Chrome): Chrome webdriver.
        """
        self.driver = driver

    def wait_for_presence(
        self, by_locator: Tuple[By, str], wait_time: int = 15
    ) -> None:
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(by_locator)
        )

    # this function performs a wait, then clicks on the web element whose locator is passed to it
    def click(self, by_locator: Tuple[By, str]):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        ).click()

    # this function asserts comparison of a web element's text with passed in text.
    def assert_element_text(
        self, by_locator: Tuple[By, str], element_text: str
    ):
        web_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        )
        assert web_element.text == element_text

    # this function performs text entry of the passed in text, in a web element whose locator is passed to it.
    def enter_text(self, by_locator: Tuple[By, str], text_to_send: str):
        return (
            WebDriverWait(self.driver, 10)
            .until(EC.visibility_of_element_located(by_locator))
            .send_keys(text_to_send)
        )

    # this function checks if the web element whose locator has been passed to it, is enabled or not and returns
    # web element if it is enabled.
    def is_enabled(self, by_locator: Tuple[By, str]):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        )

    # this function checks if the web element whose locator has been passed to it, is visible or not and returns
    # true or false depending upon its visibility.
    def is_visible(self, by_locator: Tuple[By, str]):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        )
        return bool(element)
