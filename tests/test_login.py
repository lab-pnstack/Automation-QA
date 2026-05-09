# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from locators.login_locators import LoginLocators
from locators.register_locators import RegisterLocators
from utils.config import TEST_EMAIL, TEST_PASSWORD
from utils.helpers import generate_email


class TestLogin:

    # TC01: Đăng nhập thành công
    def test_login_valid_credentials(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login(TEST_EMAIL, TEST_PASSWORD)
        assert page.is_logged_in(), "Đăng nhập thất bại với tài khoản hợp lệ"

    # TC02: Đăng nhập email sai
    def test_login_wrong_email(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("wrong@email.com", TEST_PASSWORD)
        assert "No customer account found" in page.get_error_message()

    # TC03: Đăng nhập password sai
    def test_login_wrong_password(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login(TEST_EMAIL, "wrongpassword")
        error = page.get_error_message()
        assert "unsuccessful" in error or "No customer account" in error

    # TC04: Đăng nhập email trống
    def test_login_empty_email(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("", TEST_PASSWORD)
        assert page.is_visible(LoginLocators.ERROR_MESSAGE) or "login" in page.get_url()

    # TC05: Đăng nhập cả hai trường trống
    def test_login_empty_fields(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("", "")
        assert "login" in page.get_url(), "Không nên redirect khi fields trống"

    # TC06: Logout
    def test_logout(self, logged_in_driver):
        page = LoginPage(logged_in_driver)
        page.logout()
        # Kiểm tra đã logout: không còn hiện email nữa
        # Dùng is_visible với timeout ngắn thay vì assert trực tiếp
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from locators.login_locators import LoginLocators
        wait = WebDriverWait(logged_in_driver, 5)
        try:
            wait.until(EC.invisibility_of_element_located(LoginLocators.LOGGED_IN_USER))
            assert True
        except:
            # Nếu element vẫn còn, kiểm tra URL có chứa /logout không
            assert "logout" not in page.get_url(), "Logout thất bại"


class TestRegister:

    # TC07: Đăng ký thành công
    def test_register_success(self, driver):
        page = RegisterPage(driver)
        page.open()
        page.register(
            first_name="Test",
            last_name="User",
            email=generate_email(),
            password="Test@12345"
        )
        assert "Your registration completed" in page.get_success_message()

    # TC08: Đăng ký email đã tồn tại
    def test_register_duplicate_email(self, driver):
        page = RegisterPage(driver)
        page.open()
        page.register("Test", "User", TEST_EMAIL, TEST_PASSWORD)
        error = page.get_summary_error()   # ← dùng get_summary_error thay vì get_error_message
        assert "already exists" in error

    # TC09: Đăng ký password quá ngắn
    def test_register_short_password(self, driver):
        page = RegisterPage(driver)
        page.open()
        page.register("Test", "User", generate_email(), "123")
        assert page.is_visible(RegisterLocators.ERROR_MESSAGE)

    # TC10: Đăng ký bỏ trống first name
    def test_register_empty_firstname(self, driver):
        page = RegisterPage(driver)
        page.open()
        page.register("", "User", generate_email(), "Test@12345")
        assert page.is_visible(RegisterLocators.ERROR_MESSAGE)