"""
Permission and role-based access tests — Admin menu accessibility.
"""

import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.permissions
class TestPermissions:
    """Verify authorized user can access Admin module."""

    def test_admin_menu_access_for_authenticated_user(self, authenticated_session):
        """
        Verify Admin user can navigate to Admin > System Users page.
        """
        dashboard_page = authenticated_session["dashboard_page"]

        assert dashboard_page.is_dashboard_loaded()
        dashboard_page.navigate_to_admin()

        assert dashboard_page.is_admin_page_loaded()
        assert "admin" in dashboard_page.get_current_url().lower()
        header = dashboard_page.get_admin_page_header_text()
        assert header in ("System Users", "Users", "Admin")
