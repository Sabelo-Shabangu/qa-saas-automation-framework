QA SaaS Automation Framework

This is a Selenium + PyTest automation framework built for practicing real-world QA testing using the OrangeHRM demo application.

It focuses on building a maintainable test structure using Page Object Model (POM), with reporting and basic CI/CD setup using Jenkins.

Tech Stack
Python
Selenium WebDriver
PyTest
pytest-html
webdriver-manager
Jenkins (CI/CD)
Application Under Test

OrangeHRM Demo
https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

Login:

Username: Admin
Password: admin123
What this project covers
Login testing (valid and invalid users)
Dashboard load verification after login
Basic permission check (Admin menu access)
Smoke and regression-ready test structure
Project Structure
qa-saas-automation-framework/
├── config/
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── test_login.py
│   ├── test_dashboard.py
│   └── test_permissions.py
├── utils/
├── reports/
├── screenshots/
├── conftest.py
├── pytest.ini
├── requirements.txt
└── Jenkinsfile
How to run
pip install -r requirements.txt
pytest

Run headless:

HEADLESS=true pytest
Reporting

After test execution:

HTML report is generated in /reports
Screenshots are saved in /screenshots when tests fail
Jenkins CI/CD

This project includes a Jenkins pipeline that:

Pulls the code from GitHub
Installs dependencies
Runs tests in headless mode
Generates HTML reports
Saves reports as build artifacts
QA focus of this project

This project was built to simulate real QA work, not just automation practice.

It helps demonstrate:

How test cases are structured in real projects
How POM is used to keep tests maintainable
How regression testing is organized
How CI/CD fits into QA workflows
Skills used
Selenium WebDriver automation
PyTest framework
Page Object Model (POM)
Basic CI/CD with Jenkins
Test case design and execution
Debugging failed tests
Writing reusable test code
Evidence
GitHub repo: https://github.com/Sabelo-Shabangu/qa-saas-automation-framework
Test reports: /reports

## License

Educational / portfolio use. OrangeHRM is a third-party demo application.
