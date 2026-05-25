# QA SaaS Automation Framework

Production-ready Selenium + PyTest automation framework for **OrangeHRM** open-source demo, built with Page Object Model (POM), pytest-html reporting, and Jenkins CI/CD integration.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| UI Automation | Selenium WebDriver 4.x |
| Test Runner | PyTest |
| Reporting | pytest-html |
| Driver Management | webdriver-manager |
| Design Pattern | Page Object Model (POM) |
| CI/CD | Jenkins (Declarative Pipeline) |

## Target Application

- **URL:** https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
- **Demo credentials:** `Admin` / `admin123`

## Project Structure

```
qa-saas-automation-framework/
├── config/
│   └── settings.py          # Central configuration & env overrides
├── pages/
│   ├── base_page.py         # Reusable waits & interactions
│   ├── login_page.py        # Login page object
│   └── dashboard_page.py    # Dashboard & navigation POM
├── tests/
│   ├── test_login.py        # Valid & invalid login
│   ├── test_dashboard.py    # Dashboard visibility
│   └── test_permissions.py  # Admin menu access
├── utils/
│   ├── driver_factory.py    # WebDriver factory (webdriver-manager)
│   └── logger.py            # Logging utility
├── reports/                 # Auto-generated HTML reports
├── screenshots/             # Failure screenshots
├── conftest.py              # PyTest fixtures & hooks
├── pytest.ini               # PyTest configuration
├── requirements.txt         # Python dependencies
├── Jenkinsfile              # Jenkins CI/CD pipeline
└── README.md
```

## Test Coverage

| Test | Description |
|------|-------------|
| `test_valid_login` | Successful login redirects to dashboard |
| `test_invalid_login` | Invalid credentials show error message |
| `test_login_page_is_displayed` | Login UI loads correctly |
| `test_dashboard_visibility_after_login` | Dashboard header, menu, user dropdown |
| `test_admin_menu_access_for_authenticated_user` | Admin user can open System Users |

## Prerequisites

- Python 3.10 or higher
- Google Chrome (recommended) or Mozilla Firefox
- pip

## Setup

1. **Clone or navigate to the project:**

   ```bash
   cd qa-saas-automation-framework
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Run full suite

```bash
pytest
```

### Run with visible browser

```bash
pytest --browser=chrome
```

### Run headless (CI-style)

```bash
pytest --headless
```

### Run by marker

```bash
pytest -m smoke
pytest -m regression
pytest -m login
```

### Run a single test file

```bash
pytest tests/test_login.py -v
```

## Reports

After execution, an HTML report is generated automatically:

- **Path:** `reports/report.html`
- Open in any browser for pass/fail details and execution metadata.

Failed tests also capture screenshots in `screenshots/`.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | OrangeHRM login URL | Application entry point |
| `TEST_USERNAME` | Admin | Valid username |
| `TEST_PASSWORD` | admin123 | Valid password |
| `HEADLESS` | false | Set `true` for headless mode |
| `BROWSER` | chrome | `chrome` or `firefox` |
| `EXPLICIT_WAIT` | 15 | Explicit wait timeout (seconds) |

Example:

```bash
# Windows PowerShell
$env:HEADLESS="true"
pytest

# Linux / macOS
HEADLESS=true pytest
```

## Jenkins CI/CD

The included `Jenkinsfile` defines a declarative pipeline with:

1. **Checkout** — Pull source code
2. **Setup Python Environment** — Create virtualenv
3. **Install Dependencies** — `pip install -r requirements.txt`
4. **Run Tests** — Headless pytest execution
5. **Generate HTML Report** — Verify report artifact
6. **Archive Artifacts** — Store `reports/` and `screenshots/`

### Jenkins setup notes

- Install **Python 3** and **Google Chrome** on the Jenkins agent
- Create a **Pipeline** job pointing to this repository
- Set **Pipeline script from SCM** and select the `Jenkinsfile`
- Ensure the agent has network access to OrangeHRM demo and ChromeDriver download (webdriver-manager)

## Framework Design Highlights

- **Page Object Model** — Maintainable, reusable page classes
- **Explicit waits only** — No `time.sleep()`; WebDriverWait throughout
- **Driver factory** — Centralized browser setup with webdriver-manager
- **PyTest fixtures** — Driver lifecycle, login session, failure screenshots
- **Logging** — Structured console logging for debugging
- **Markers** — Smoke vs regression suite selection for CI tiers

## License

Educational / portfolio use. OrangeHRM is a third-party demo application.
