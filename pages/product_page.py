# pages/product_page.py
from pages.base_page import BasePage
from locators.product_locators import ProductLocators
from utils.config import BASE_URL
from selenium.webdriver.support.ui import Select

class ProductPage(BasePage):

    # ── Navigation ──────────────────────────────────────────
    def open_homepage(self):
        self.navigate(BASE_URL)

    def open_category(self, path):
        """Mở category theo path, vd: '/books', '/computers' """
        self.navigate(f"{BASE_URL}{path}")

    def get_nav_menu_items(self):
        """Lấy danh sách tên các menu item."""
        items = self.driver.find_elements(*ProductLocators.NAV_MENU_ITEMS)
        return [item.text for item in items]

    # ── Search ───────────────────────────────────────────────
    def search(self, keyword):
        self.type(ProductLocators.SEARCH_INPUT, keyword)
        self.click(ProductLocators.SEARCH_BUTTON)

    def get_search_results(self):
        """Trả về list tên sản phẩm tìm được."""
        try:
            items = self.driver.find_elements(*ProductLocators.PRODUCT_TITLES)
            return [item.text for item in items]
        except:
            return []

    def is_no_result_shown(self):
        return self.is_visible(ProductLocators.SEARCH_NO_RESULT)

    def get_result_count(self):
        items = self.driver.find_elements(*ProductLocators.PRODUCT_GRID_ITEMS)
        return len(items)

    # ── Product detail ───────────────────────────────────────
    def click_first_product(self):
        self.click(ProductLocators.FIRST_PRODUCT)

    def click_product_by_name(self, name):
        titles = self.driver.find_elements(*ProductLocators.PRODUCT_TITLES)
        for title in titles:
            if name.lower() in title.text.lower():
                title.click()
                return
        raise Exception(f"Không tìm thấy sản phẩm: {name}")

    def get_product_name(self):
        return self.get_text(ProductLocators.PRODUCT_NAME)

    def get_product_price(self):
        return self.get_text(ProductLocators.PRODUCT_PRICE)

    def get_product_sku(self):
        return self.get_text(ProductLocators.PRODUCT_SKU)

    def is_add_to_cart_visible(self):
        return self.is_visible(ProductLocators.ADD_TO_CART_BTN)

    def is_add_to_wishlist_visible(self):
        return self.is_visible(ProductLocators.ADD_TO_WISHLIST)

    # ── Filter & Sort ────────────────────────────────────────
    def sort_by(self, option_text):
        """option_text: 'Name: A to Z', 'Price: Low to High', ..."""
        select = Select(self.find(ProductLocators.SORT_DROPDOWN))
        select.select_by_visible_text(option_text)
        self._pause(1.5)

    def set_page_size(self, size):
        """size: '4', '8', '12'"""
        select = Select(self.find(ProductLocators.PAGE_SIZE_SELECT))
        select.select_by_visible_text(str(size))
        self._pause(1.5)

    def get_all_product_names(self):
        items = self.driver.find_elements(*ProductLocators.PRODUCT_TITLES)
        return [i.text for i in items]

    def get_all_product_prices(self):
        prices = self.driver.find_elements(*ProductLocators.PRODUCT_PRICES)
        result = []
        for p in prices:
            try:
                result.append(float(p.text.replace(",", "").strip()))
            except:
                pass
        return result