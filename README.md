# Pytest_playwright_allure

## Setup

Use Python 3.9 or newer. Install dependencies and the Playwright Chromium browser:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Create a `.env` file in the project root with `LOGIN` and `PASSWORD`.
Selenium uses the installed Google Chrome; Playwright uses its downloaded Chromium.
The existing Alpine Docker image is for Selenium; Playwright needs a supported
OS image (for example, the official Playwright Python Ubuntu image).

## Run tests

Run from the project root. Selenium is the default engine unless
`PLAYWRIGHT_DEBUG=true` is set:

```bash
python -m pytest tests/feature_profile_test.py --engine=selenium -v -s
python -m pytest tests/feature_profile_test.py --engine=playwright -v -s
```

Add `--headless` to either command to run without a browser window.
The same test and Page Objects support both engines. Each test receives a new
Selenium session or an isolated Playwright browser context, closed after the test.
The profile test updates the name on the configured account.

## Allure

```bash
python -m pytest tests/feature_profile_test.py --engine=playwright --headless --alluredir=allure-results
allure serve allure-results
```

The Allure CLI must be installed separately to view reports.

## Local debugging in PyCharm

Set this flag in the project-root `.env` to select Playwright without CLI arguments:

```dotenv
PLAYWRIGHT_DEBUG=true
```

Run or Debug the pytest test in PyCharm using the project's `venv` interpreter.
The browser opens with a visible window unless `--headless` is provided.
The flag applies to local terminal runs as well; it does not detect the IDE debugger
or open Playwright Inspector. Set it to `false` to restore Selenium as the default.
An explicit `--engine=selenium` or `--engine=playwright` always takes precedence.
The `.env` file is loaded relative to `conftest.py`, independently of the working directory.
