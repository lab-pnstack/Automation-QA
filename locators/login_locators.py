# locators/login_locators.py
from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT    = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")
    LOGIN_BUTTON   = (By.CSS_SELECTOR, "input.login-button")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, ".validation-summary-errors")
    LOGOUT_LINK    = (By.CSS_SELECTOR, "a[href='/logout']")
    MY_ACCOUNT     = (By.CSS_SELECTOR, "a[href='/customer/info']")
    LOGGED_IN_USER = (By.CSS_SELECTOR, "a.account")  # Hiện email khi đã login  