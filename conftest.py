"""
PyTest fixtures and hooks for the QA SaaS automation framework.
Provides WebDriver lifecycle, authenticated session, and failure screenshots.
"""

from datetime import datetime

import pytest

from config.settings import (
    BASE_URL,
    HEADLESS,
    IMPLICIT_WAIT,
    SCREENSHOTS_DIR,
    VALID_PASSWORD,
    VALID_USERNAME,
)
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory
from utils.logger import get_logger

logger = get_logger(__name__)


def pytest_addoption(parser):
    """Register custom CLI options for local and CI execution."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=HEADLESS,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome or firefox",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped WebDriver fixture.
    Creates driver before each test and quits after completion.
    """
    headless = request.config.getoption("--headless")
    browser = request.config.getoption("--browser")

    logger.info("Starting WebDriver fixture (browser=%s, headless=%s)", browser, headless)
    web_driver = DriverFactory.create_driver(browser=browser, headless=headless)

    if IMPLICIT_WAIT > 0:
        web_driver.implicitly_wait(IMPLICIT_WAIT)

    yield web_driver

    logger.info("Tearing down WebDriver fixture")
    web_driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """Provide a LoginPage instance navigated to the application."""
    page = LoginPage(driver)
    page.navigate()
    return page


@pytest.fixture(scope="function")
def authenticated_session(driver):
    """
    Log in with valid credentials and return page objects for dependent tests.
    Reduces duplication across dashboard and permission tests.
    """
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    dashboard_page = DashboardPage(driver)
    dashboard_page.wait_for_dashboard_url()

    return {
        "driver": driver,
        "login_page": login_page,
        "dashboard_page": dashboard_page,
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture test outcome for screenshot-on-failure hook.
    Stores report on the item for use in the driver fixture teardown.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(scope="function", autouse=True)
def capture_screenshot_on_failure(request, driver):
    """Save a screenshot when a test fails during the call phase."""
    yield

    report = getattr(request.node, "rep_call", None)
    if report is None or report.passed:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = request.node.name.replace("/", "_").replace("\\", "_")
    screenshot_path = SCREENSHOTS_DIR / f"{test_name}_{timestamp}.png"

    try:
        driver.save_screenshot(str(screenshot_path))
        logger.error("Test failed. Screenshot saved: %s", screenshot_path)
    except Exception as exc:
        logger.error("Could not capture screenshot: %s", exc)


def pytest_html_report_title(report):
    """Customize pytest-html report title."""
    report.title = "OrangeHRM QA Automation Report"


def pytest_configure(config):
    """Log framework configuration at session start."""
    logger.info("Test session started | BASE_URL=%s", BASE_URL)
