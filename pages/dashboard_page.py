import allure
from base.base_page import BasePage
from config.links import Links


class DashboardPage(BasePage):
    PAGE_URL = Links.DASHBOARD_PAGE
    MY_INFO_BUTTON = ("xpath", "//span[text()='My Info']")

    @allure.step("Click on 'My Info' link")
    def click_my_info_link(self):
        self.click(self.MY_INFO_BUTTON)