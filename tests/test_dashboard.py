"""
Dashboard validation test suite — post-login UI visibility checks.
"""

import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.dashboard
class TestDashboard:
    """Dashboard visibility and navigation tests."""

    def test_dashboard_visibility_after_login(self, authenticated_session):
        """
        Verify core dashboard elements are visible after successful login.
        """
        dashboard_page = authenticated_session["dashboard_page"]

        assert dashboard_page.is_dashboard_loaded()
        assert dashboard_page.get_dashboard_header_text() == "Dashboard"
        assert dashboard_page.is_user_dropdown_visible()
        assert dashboard_page.is_side_menu_visible()
        assert "dashboard" in dashboard_page.get_current_url().lower()
