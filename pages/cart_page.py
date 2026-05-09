# pages/cart_page.py
from pages.base_page import BasePage
from locators.cart_locators import CartLocators
from locators.product_locators import ProductLocators
from utils.config import BASE_URL
from selenium.webdriver.common.by import By

class CartPage(BasePage):

    def open_cart(self):
        self.navigate(f"{BASE_URL}/cart")

    def open_product(self, path):
        self.navigate(f"{BASE_URL}{path}")

    # ── Add to cart ──────────────────────────────────────────
    def add_to_cart(self):
        self.click(CartLocators.ADD_TO_CART_BTN)
        self._pause(2)

    def set_quantity_before_add(self, qty):
        self.type(CartLocators.QTY_INPUT, str(qty))

    def get_notification_text(self):
        return self.get_text(CartLocators.SUCCESS_NOTIFICATION)

    def go_to_cart(self):
        self.click(CartLocators.CART_LINK)
        self._pause(1.5)

    # ── Cart info ────────────────────────────────────────────
    def get_cart_item_count(self):
        items = self.driver.find_elements(*CartLocators.CART_PAGE_ITEMS)
        return len(items)

    def get_cart_item_names(self):
        items = self.driver.find_elements(*CartLocators.CART_ITEM_NAMES)
        return [i.text for i in items]

    def get_cart_total(self):
        return self.get_text(CartLocators.CART_TOTAL)

    def is_cart_empty(self):
        """Kiểm tra cart trống bằng cách đếm số item = 0."""
        items = self.driver.find_elements(*CartLocators.CART_PAGE_ITEMS)
        return len(items) == 0       # ← FIX: đếm item thay vì tìm element trống

    def get_item_qty(self, index=0):
        inputs = self.driver.find_elements(*CartLocators.CART_QTY_INPUTS)
        return inputs[index].get_attribute("value")

    # ── Update quantity ──────────────────────────────────────
    def update_quantity(self, index=0, new_qty=2):
        inputs = self.driver.find_elements(*CartLocators.CART_QTY_INPUTS)
        inputs[index].clear()
        inputs[index].send_keys(str(new_qty))
        self._pause(0.5)
        self.click(CartLocators.UPDATE_CART_BTN)
        self._pause(2)

    # ── Remove product ───────────────────────────────────────
    def remove_item(self, index=0):
        checkboxes = self.driver.find_elements(*CartLocators.REMOVE_CHECKBOX)
        checkboxes[index].click()
        self._pause(0.5)
        self.click(CartLocators.UPDATE_CART_BTN)
        self._pause(2)

    def remove_all_items(self):
        checkboxes = self.driver.find_elements(*CartLocators.REMOVE_CHECKBOX)
        if not checkboxes:          # ← FIX: nếu cart trống thì bỏ qua
            return
        for cb in checkboxes:
            cb.click()
            self._pause(0.3)
        self.click(CartLocators.UPDATE_CART_BTN)
        self._pause(2)

    # ── Checkout ─────────────────────────────────────────────
    def click_checkout(self):
        self.click(CartLocators.TERMS_CHECKBOX)
        self._pause(0.5)
        self.click(CartLocators.CHECKOUT_BTN)
        self._pause(2)