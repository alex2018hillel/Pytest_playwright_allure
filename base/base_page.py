import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, engine="selenium"):
        self.driver = driver
        self.engine = engine
        if engine == "selenium":
            self.wait = WebDriverWait(driver, 10, poll_frequency=1)
        elif engine == "playwright":
            self.driver.set_default_timeout(10000)

    def _locator(self, locator):
        strategy, selector = locator
        if strategy == "xpath":
            return self.driver.locator("xpath=" + selector)
        if strategy == "css selector":
            return self.driver.locator(selector)
        raise ValueError("Unsupported locator strategy: " + strategy)

    def wait_for_element(self, locator, timeout=10):
        """Wait for a visible element; timeout is in seconds."""
        if self.engine == "playwright":
            element = self._locator(locator)
            element.wait_for(state="visible", timeout=timeout * 1000)
            return element
        return WebDriverWait(self.driver, timeout, poll_frequency=1).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        if self.engine == "playwright":
            self.wait_for_element(locator)
            self._locator(locator).click()
        else:
            self.wait.until(EC.element_to_be_clickable(locator)).click()

    def fill(self, locator, value):
        if self.engine == "playwright":
            self.click(locator)
            self._locator(locator).fill(value)
        else:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.clear()
            element.send_keys(value)

    def wait_for_hidden(self, locator):
        if self.engine == "playwright":
            self._locator(locator).wait_for(state="hidden")
        else:
            self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_value(self, locator, value):
        if self.engine == "playwright":
            from playwright.sync_api import expect
            expect(self._locator(locator)).to_have_value(value, timeout=10000)
        else:
            self.wait.until(EC.visibility_of_element_located(locator))
            self.wait.until(lambda driver: driver.find_element(*locator).get_attribute("value") == value)

    def open(self):
        with allure.step(f"Open {self.PAGE_URL} page"):
            if self.engine == "playwright":
                self.driver.goto(self.PAGE_URL)
            else:
                self.driver.get(self.PAGE_URL)

    def is_opened(self):
        with allure.step(f"Page {self.PAGE_URL} is opened"):
            if self.engine == "playwright":
                from playwright.sync_api import expect
                expect(self.driver).to_have_url(self.PAGE_URL, timeout=10000)
            else:
                self.wait.until(EC.url_to_be(self.PAGE_URL))

    def make_screenshot(self, screenshot_name):
        screenshot = (
            self.driver.screenshot() if self.engine == "playwright"
            else self.driver.get_screenshot_as_png()
        )
        allure.attach(body=screenshot, name=screenshot_name, attachment_type=AttachmentType.PNG)
