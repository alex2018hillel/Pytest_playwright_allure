import allure
from base.base_page import BasePage
from config.links import Links


class PersonalPage(BasePage):
    PAGE_URL = Links.PERSONAL_PAGE
    FIRST_NAME_FIELD = ("xpath", "//input[@name='firstName']")
    SAVE_BUTTON = ("xpath", "(//button[@type='submit'])[1]")
    SPINNER = ("xpath", "//div[@class='oxd-loading-spinner']")

    def change_name(self, new_name):
        with allure.step(f"Change name on '{new_name}'"):
            self.wait_for_element(self.FIRST_NAME_FIELD)
            self.fill(self.FIRST_NAME_FIELD, new_name)
            self.name = new_name

    @allure.step("Save changes")
    def save_changes(self):
        self.click(self.SAVE_BUTTON)

    @allure.step("Changes has been saved successfuly")
    def is_changes_saved(self):
        self.wait_for_hidden(self.SPINNER)
        self.wait_for_value(self.FIRST_NAME_FIELD, self.name)
