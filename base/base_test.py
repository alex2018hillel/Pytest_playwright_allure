import pytest
from config.data import Data
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.personal_page import PersonalPage


class BaseTest:

    data: Data

    login_page: LoginPage
    dashboard_page: DashboardPage
    personal_page: PersonalPage

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver
        request.cls.data = Data()

        engine = request.config.getoption("--engine")
        request.cls.login_page = LoginPage(driver, engine)
        request.cls.dashboard_page = DashboardPage(driver, engine)
        request.cls.personal_page = PersonalPage(driver, engine)
