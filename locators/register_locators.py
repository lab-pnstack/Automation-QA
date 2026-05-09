# locators/register_locators.py
from selenium.webdriver.common.by import By

class RegisterLocators:
    GENDER_MALE      = (By.ID, "gender-male")
    FIRST_NAME       = (By.ID, "FirstName")
    LAST_NAME        = (By.ID, "LastName")
    EMAIL_INPUT      = (By.ID, "Email")
    PASSWORD_INPUT   = (By.ID, "Password")
    CONFIRM_PASSWORD = (By.ID, "ConfirmPassword")
    REGISTER_BUTTON  = (By.ID, "register-button")
    SUCCESS_MESSAGE  = (By.CSS_SELECTOR, ".result")
    ERROR_MESSAGE    = (By.CSS_SELECTOR, ".field-validation-error")
    REGISTER_LINK    = (By.CSS_SELECTOR, "a[href='/register']")