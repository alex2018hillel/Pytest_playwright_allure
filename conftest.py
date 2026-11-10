import os
from pathlib import Path

import pytest
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")


def pytest_addoption(parser):
    group = parser.getgroup("browser")
    group.addoption(
        "--engine", choices=("selenium", "playwright"), default=(
            "playwright"
            if os.getenv("PLAYWRIGHT_DEBUG", "").strip().lower() in ("1", "true", "yes", "on")
            else "selenium"
        ),
        help="Browser engine (default: playwright when PLAYWRIGHT_DEBUG=true, otherwise selenium)",
    )
    group.addoption("--headless", action="store_true", help="Run without a browser window")


@pytest.fixture(scope="function")
def driver(request):
    engine = request.config.getoption("--engine")
    headless = request.config.getoption("--headless")
    if engine == "playwright":
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as error:
            raise pytest.UsageError(
                "Playwright is not installed. Run: python -m pip install -r requirements.txt "
                "and python -m playwright install chromium"
            ) from error
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless)
            try:
                context = browser.new_context()
                try:
                    page = context.new_page()
                    page.set_default_timeout(10000)
                    yield page
                finally:
                    context.close()
            finally:
                browser.close()
    else:
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(options=options)
        try:
            yield browser
        finally:
            browser.quit()
