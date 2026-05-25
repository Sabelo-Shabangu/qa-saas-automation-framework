"""
Login page object for OrangeHRM authentication module.
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object representing the OrangeHRM login screen."""

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CREDENTIALS_ERROR = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    LOGIN_PANEL = (By.CSS_SELECTOR, ".orangehrm-login-slot")
    LOGIN_TITLE = (By.CSS_SELECTOR, ".orangehrm-login-title")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = BASE_URL

    def navigate(self) -> "LoginPage":
        """Open the login page."""
        self.open(self.url)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Perform a full login flow with credentials."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_login_page_displayed(self) -> bool:
        return self.is_displayed(self.LOGIN_PANEL)

    def get_credentials_error_message(self) -> str:
        return self.get_text(self.CREDENTIALS_ERROR)

    def is_credentials_error_displayed(self) -> bool:
        return self.is_displayed(self.CREDENTIALS_ERROR)

    def get_login_title(self) -> str:
        return self.get_text(self.LOGIN_TITLE)
