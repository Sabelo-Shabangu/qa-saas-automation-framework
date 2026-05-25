"""
Central configuration for the OrangeHRM automation framework.
Environment variables override defaults for CI/CD flexibility.
"""

import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Application under test
BASE_URL = os.getenv(
    "BASE_URL",
    "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
)

# Valid demo credentials (OrangeHRM open-source demo)
VALID_USERNAME = os.getenv("TEST_USERNAME", "Admin")
VALID_PASSWORD = os.getenv("TEST_PASSWORD", "admin123")
INVALID_USERNAME = os.getenv("INVALID_USERNAME", "InvalidUser")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD", "wrongpassword")

# Browser settings
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
# Optional: point to a pre-installed driver binary (skips webdriver-manager download)
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "")
GECKODRIVER_PATH = os.getenv("GECKODRIVER_PATH", "")
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "0"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))

# Output directories
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Ensure output directories exist at import time
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
