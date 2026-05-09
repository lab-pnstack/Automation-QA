# pages/login_page.py
from pages.base_page import BasePage
from locators.login_locators import LoginLocators
from utils.config import BASE_URL
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):

    def open(self):
        self.navigate(f"{BASE_URL}/login")

    def login(self, email, password):
        self.type(LoginLocators.EMAIL_INPUT, email)
        self.type(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(LoginLocators.ERROR_MESSAGE)

    def is_logged_in(self):
        return self.is_visible(LoginLocators.LOGGED_IN_USER)

    def logout(self):
        self.click(LoginLocators.LOGOUT_LINK)
        # Chờ redirect về trang chủ sau logout
        self.wait.until(EC.url_contains(BASE_URL))

    def get_logged_in_email(self):
        return self.get_text(LoginLocators.LOGGED_IN_USER)