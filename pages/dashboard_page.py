"""
Dashboard and navigation page objects for post-login OrangeHRM flows.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object for the OrangeHRM dashboard and sidebar navigation."""

    # Locators
    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[contains(@class,'oxd-text') and normalize-space()='Dashboard']",
    )
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    SIDE_MENU = (By.CSS_SELECTOR, ".oxd-sidepanel-body")
    ADMIN_MENU_ITEM = (
        By.XPATH,
        "//span[contains(@class,'oxd-main-menu-item--name') and normalize-space()='Admin']",
    )
    ADMIN_PAGE_HEADER = (
        By.XPATH,
        "//h6[contains(@class,'oxd-text') and (normalize-space()='System Users' "
        "or normalize-space()='Users')]",
    )
    ADMIN_USER_TABLE = (By.CSS_SELECTOR, ".oxd-table-body")
    ADMIN_ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    BREADCRUMB_DASHBOARD = (
        By.XPATH,
        "//span[contains(@class,'oxd-topbar-body-nav-tab-item') and normalize-space()='Dashboard']",
    )

    def is_dashboard_loaded(self) -> bool:
        """Return True when the dashboard header is visible."""
        return self.is_displayed(self.DASHBOARD_HEADER)

    def get_dashboard_header_text(self) -> str:
        return self.get_text(self.DASHBOARD_HEADER)

    def is_user_dropdown_visible(self) -> bool:
        return self.is_displayed(self.USER_DROPDOWN)

    def is_side_menu_visible(self) -> bool:
        return self.is_displayed(self.SIDE_MENU)

    def navigate_to_admin(self) -> None:
        """Click Admin menu item in the sidebar."""
        self.click(self.ADMIN_MENU_ITEM)
        self.wait_for_url_contains("admin")

    def is_admin_page_loaded(self) -> bool:
        """Return True when Admin module (System Users) is displayed."""
        if "admin" not in self.get_current_url().lower():
            return False
        return (
            self.is_displayed(self.ADMIN_PAGE_HEADER)
            or self.is_displayed(self.ADMIN_USER_TABLE)
            or self.is_displayed(self.ADMIN_ADD_BUTTON)
        )

    def get_admin_page_header_text(self) -> str:
        if self.is_displayed(self.ADMIN_PAGE_HEADER):
            return self.get_text(self.ADMIN_PAGE_HEADER)
        return "Admin"

    def wait_for_dashboard_url(self) -> None:
        self.wait_for_url_contains("dashboard")
