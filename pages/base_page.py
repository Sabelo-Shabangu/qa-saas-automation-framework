"""
Base page class providing reusable Selenium interactions with explicit waits.
All page objects inherit from this class to ensure consistent behavior.
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import EXPLICIT_WAIT
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Base class for all Page Object Model implementations."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def open(self, url: str) -> None:
        """Navigate to the given URL."""
        logger.info("Navigating to: %s", url)
        self.driver.get(url)

    def find_element(self, locator: tuple[By, str]) -> WebElement:
        """Wait for and return a visible element."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator: tuple[By, str]) -> list[WebElement]:
        """Wait for and return all matching visible elements."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple[By, str]) -> None:
        """Wait until element is clickable, then click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        logger.info("Clicking element: %s", locator[1])
        element.click()

    def type_text(self, locator: tuple[By, str], text: str, clear_first: bool = True) -> None:
        """Wait for element, optionally clear, then send keys."""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        logger.info("Typing into element: %s", locator[1])
        element.send_keys(text)

    def get_text(self, locator: tuple[By, str]) -> str:
        """Return visible text from an element."""
        return self.find_element(locator).text.strip()

    def is_displayed(self, locator: tuple[By, str]) -> bool:
        """Return True if element is visible within the explicit wait timeout."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment: str) -> None:
        """Wait until the current URL contains the given fragment."""
        self.wait.until(EC.url_contains(fragment))

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Return the browser page title."""
        return self.driver.title
