"""
WebDriver factory using webdriver-manager for automatic driver management.
Supports headless execution for Jenkins CI/CD pipelines.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.settings import (
    BROWSER,
    CHROMEDRIVER_PATH,
    GECKODRIVER_PATH,
    HEADLESS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def _resolve_chrome_service() -> ChromeService:
    """Resolve ChromeDriver service: env path, webdriver-manager, or Selenium Manager."""
    if CHROMEDRIVER_PATH:
        logger.info("Using ChromeDriver from CHROMEDRIVER_PATH")
        return ChromeService(executable_path=CHROMEDRIVER_PATH)

    try:
        driver_path = ChromeDriverManager().install()
        return ChromeService(driver_path)
    except Exception as exc:
        logger.warning(
            "webdriver-manager could not provision ChromeDriver (%s). "
            "Falling back to Selenium Manager.",
            exc,
        )
        return ChromeService()


def _resolve_firefox_service() -> FirefoxService:
    """Resolve GeckoDriver service: env path, webdriver-manager, or Selenium Manager."""
    if GECKODRIVER_PATH:
        logger.info("Using GeckoDriver from GECKODRIVER_PATH")
        return FirefoxService(executable_path=GECKODRIVER_PATH)

    try:
        driver_path = GeckoDriverManager().install()
        return FirefoxService(driver_path)
    except Exception as exc:
        logger.warning(
            "webdriver-manager could not provision GeckoDriver (%s). "
            "Falling back to Selenium Manager.",
            exc,
        )
        return FirefoxService()


class DriverFactory:
    """Factory class responsible for creating and configuring WebDriver instances."""

    @staticmethod
    def create_driver(browser: str | None = None, headless: bool | None = None) -> webdriver.Remote:
        """
        Create and return a configured WebDriver instance.

        Args:
            browser: Browser name ('chrome' or 'firefox'). Defaults to settings.BROWSER.
            headless: Run in headless mode. Defaults to settings.HEADLESS.

        Returns:
            Configured WebDriver instance.
        """
        browser_name = (browser or BROWSER).lower()
        run_headless = HEADLESS if headless is None else headless

        logger.info("Initializing %s WebDriver (headless=%s)", browser_name, run_headless)

        if browser_name == "chrome":
            driver = DriverFactory._create_chrome_driver(run_headless)
        elif browser_name == "firefox":
            driver = DriverFactory._create_firefox_driver(run_headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        logger.info("WebDriver initialized successfully")
        return driver

    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=%d,%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))

        if headless:
            options.add_argument("--headless=new")

        service = _resolve_chrome_service()
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")

        service = _resolve_firefox_service()
        return webdriver.Firefox(service=service, options=options)
