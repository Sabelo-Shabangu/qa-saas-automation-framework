"""
Login module test suite — valid and invalid authentication scenarios.
"""

import pytest

from config.settings import (
    INVALID_PASSWORD,
    INVALID_USERNAME,
    VALID_PASSWORD,
    VALID_USERNAME,
)
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.login
class TestLogin:
    """Authentication tests for OrangeHRM login page."""

    def test_valid_login(self, login_page, driver):
        """
        Verify that valid credentials redirect the user to the dashboard.
        """
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        dashboard_page = DashboardPage(driver)
        dashboard_page.wait_for_dashboard_url()

        assert "dashboard" in dashboard_page.get_current_url().lower()
        assert dashboard_page.is_dashboard_loaded()
        assert dashboard_page.get_dashboard_header_text() == "Dashboard"

    def test_invalid_login(self, login_page):
        """
        Verify that invalid credentials show an error and keep user on login.
        """
        login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        assert login_page.is_credentials_error_displayed()
        error_message = login_page.get_credentials_error_message()
        assert "Invalid" in error_message
        assert "dashboard" not in login_page.get_current_url().lower()

    def test_login_page_is_displayed(self, login_page):
        """Verify login page UI elements are visible before authentication."""
        assert login_page.is_login_page_displayed()
        assert login_page.get_login_title() == "Login"
