# pages/register_page.py
from pages.base_page import BasePage
from locators.register_locators import RegisterLocators
from locators.login_locators import LoginLocators
from utils.config import BASE_URL

class RegisterPage(BasePage):

    def open(self):
        self.navigate(f"{BASE_URL}/register")

    def register(self, first_name, last_name, email, password):
        self.click(RegisterLocators.GENDER_MALE)
        self.type(RegisterLocators.FIRST_NAME, first_name)
        self.type(RegisterLocators.LAST_NAME, last_name)
        self.type(RegisterLocators.EMAIL_INPUT, email)
        self.type(RegisterLocators.PASSWORD_INPUT, password)
        self.type(RegisterLocators.CONFIRM_PASSWORD, password)
        self.click(RegisterLocators.REGISTER_BUTTON)

    def get_success_message(self):
        return self.get_text(RegisterLocators.SUCCESS_MESSAGE)

    def get_field_error(self):
        """Lỗi từng field: password ngắn, thiếu tên..."""
        return self.get_text(RegisterLocators.ERROR_MESSAGE)

    def get_summary_error(self):
        """Lỗi tổng: email đã tồn tại (dùng cùng class với login error)."""
        return self.get_text(LoginLocators.ERROR_MESSAGE)