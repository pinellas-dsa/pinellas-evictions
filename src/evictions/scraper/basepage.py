from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """This class is the parent class for all the pages in the scraper. It
    contains all common elements and functionalities available to all pages."""

    def __init__(self, driver: webdriver.Chrome, default_wait_time: int = 15):
        """Initializes the page.

        Args:
            driver (webdriver.Chrome): Chrome webdriver.
        """
        self.driver = driver
        self.default_wait_time = default_wait_time

    def wait_for_presence(
        self, by_locator: Tuple[By, str], wait_time: int = 15
    ) -> None:
        """Use when a only a wait is needed.

        Args:
            by_locator (Tuple[By, str]): Locator for the element to be waited for
            wait_time (int, optional): Seconds to wait before timeout. Defaults to 15.
        """
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(by_locator)
        )

    def click(self, by_locator: Tuple[By, str]) -> None:
        """Performs a wait, then clicks on the web element whose locator is passed to it

        Args:
            by_locator (Tuple[By, str]): Locator for the element to be clicked on
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        ).click()

    def assert_element_text(
        self, by_locator: Tuple[By, str], element_text: str
    ) -> None:
        """For testing. Asserts comparison of a web element's text with passed-in text.

        Args:
            by_locator (Tuple[By, str]): Locator for the element to be checked
            element_text (str): Text to be compared
        """
        web_element = WebDriverWait(self.driver, self.default_wait_time).until(
            EC.visibility_of_element_located(by_locator)
        )
        assert web_element.text == element_text

    def enter_text(self, by_locator: Tuple[By, str], text_to_send: str):
        """A wrapper for send_text that also performs a wait

        Args:
            by_locator (Tuple[By, str]): Locator for the input field to have text entered
            text_to_send (str): The text to be entered in the field

        Returns:
            _type_: I'm not sure exactly how to type this.
        """
        return (
            WebDriverWait(self.driver, self.default_wait_time)
            .until(EC.visibility_of_element_located(by_locator))
            .send_keys(text_to_send)
        )

    def is_enabled(self, by_locator: Tuple[By, str]):
        """Checks if the web element whose locator has been passed to it
        is enabled or not and returns the web element if it is enabled.

        Args:
            by_locator (Tuple[By, str]): The Locator for the element to be checked

        Returns:
            _type_: I'm not sure exactly how to type this.
        """
        return WebDriverWait(self.driver, self.default_wait_time).until(
            EC.visibility_of_element_located(by_locator)
        )

    def is_visible(self, by_locator: Tuple[By, str]) -> bool:
        """Checks if the web element whose locator has been passed to it
        is visible or not and returns true or false depending upon its visibility.

        Args:
            by_locator (Tuple[By, str]): _description_

        Returns:
            bool: True/false value, is the element visible?
        """
        element = WebDriverWait(self.driver, self.default_wait_time).until(
            EC.visibility_of_element_located(by_locator)
        )
        return bool(element)
