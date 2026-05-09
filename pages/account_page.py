# pages/account_page.py
from pages.base_page import BasePage
from utils.config import BASE_URL
from selenium.webdriver.common.by import By


class AccountLocators:
    # Wishlist
    WISHLIST_LINK        = (By.CSS_SELECTOR, "a[href='/wishlist']")
    WISHLIST_ITEMS       = (By.CSS_SELECTOR, ".cart-item-row")
    WISHLIST_ADD_BTN     = (By.CSS_SELECTOR, "input.add-to-wishlist-button")
    WISHLIST_REMOVE      = (By.CSS_SELECTOR, "input[name='removefromcart']")
    WISHLIST_UPDATE      = (By.CSS_SELECTOR, "input[name='updatecart']")
    WISHLIST_EMPTY_MSG   = (By.CSS_SELECTOR, ".order-summary-content .no-data")

    # Order history
    ORDER_HISTORY_LINK   = (By.CSS_SELECTOR, "a[href='/customer/orders']")
    ORDER_ITEMS          = (By.XPATH, "//*[contains(text(),'Order Number')]")
    ORDER_DETAILS_BTN    = (By.XPATH, "//a[contains(@href,'/customer/order/')]")
    ORDER_STATUS         = (By.CSS_SELECTOR, ".order-status")

    # Change password
    OLD_PASSWORD         = (By.ID, "OldPassword")
    NEW_PASSWORD         = (By.ID, "NewPassword")
    CONFIRM_NEW_PASSWORD = (By.ID, "ConfirmNewPassword")
    CHANGE_PWD_BTN       = (By.CSS_SELECTOR, "input.change-password-button")
    PWD_SUCCESS_MSG      = (By.CSS_SELECTOR, ".result")
    PWD_ERROR_MSG        = (By.CSS_SELECTOR, ".field-validation-error")

    # Account info
    ACCOUNT_INFO_LINK    = (By.CSS_SELECTOR, "a[href='/customer/info']")
    FIRST_NAME           = (By.ID, "FirstName")
    LAST_NAME            = (By.ID, "LastName")
    EMAIL_FIELD          = (By.ID, "Email")
    SAVE_INFO_BTN        = (By.CSS_SELECTOR, "input.save-customer-info-button")


class AccountPage(BasePage):

    # ── Navigation ───────────────────────────────────────────
    def open_wishlist(self):
        self.navigate(f"{BASE_URL}/wishlist")

    def open_order_history(self):
        self.navigate(f"{BASE_URL}/customer/orders")

    def open_change_password(self):
        self.navigate(f"{BASE_URL}/customer/changepassword")

    def open_account_info(self):
        self.navigate(f"{BASE_URL}/customer/info")

    # ── Wishlist ─────────────────────────────────────────────
    def add_to_wishlist(self, product_path):
        """Vào trang sản phẩm và click Add to wishlist."""
        self.navigate(f"{BASE_URL}{product_path}")
        self._pause(1)
        self.click(AccountLocators.WISHLIST_ADD_BTN)
        self._pause(2)

    def get_wishlist_count(self):
        items = self.driver.find_elements(*AccountLocators.WISHLIST_ITEMS)
        return len(items)

    def is_wishlist_empty(self):
        items = self.driver.find_elements(*AccountLocators.WISHLIST_ITEMS)
        return len(items) == 0

    def remove_from_wishlist(self):
        checkboxes = self.driver.find_elements(*AccountLocators.WISHLIST_REMOVE)
        if checkboxes:
            checkboxes[0].click()
            self._pause(0.5)
            self.click(AccountLocators.WISHLIST_UPDATE)
            self._pause(2)

    # ── Order history ─────────────────────────────────────────
    def get_order_count(self):
        orders = self.driver.find_elements(*AccountLocators.ORDER_ITEMS)
        return len(orders)

    def get_first_order_status(self):
        try:
            status = self.driver.find_elements(*AccountLocators.ORDER_STATUS)
            return status[0].text if status else ""
        except:
            return ""

    def click_order_details(self, index=0):
        btns = self.driver.find_elements(*AccountLocators.ORDER_DETAILS_BTN)
        if btns:
            btns[index].click()
            self._pause(2)

    # ── Change password ───────────────────────────────────────
    def change_password(self, old_pwd, new_pwd):
        self.type(AccountLocators.OLD_PASSWORD,         old_pwd)
        self.type(AccountLocators.NEW_PASSWORD,         new_pwd)
        self.type(AccountLocators.CONFIRM_NEW_PASSWORD, new_pwd)
        self.click(AccountLocators.CHANGE_PWD_BTN)
        self._pause(2)

    def get_password_success_msg(self):
        return self.get_text(AccountLocators.PWD_SUCCESS_MSG)

    def get_password_error_msg(self):
        return self.get_text(AccountLocators.PWD_ERROR_MSG)

    def is_password_changed_successfully(self):
        return self.is_visible(AccountLocators.PWD_SUCCESS_MSG)