# tests/test_checkout.py
import pytest
from pages.checkout_page import CheckoutPage
from pages.cart_page import CartPage

PRODUCT_URL = "/health"


def add_product_to_cart(driver):
    cart = CartPage(driver)
    cart.open_product(PRODUCT_URL)
    cart.add_to_cart()
    cart.open_cart()


class TestCheckoutFlow:

    def test_full_checkout_success(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.do_full_checkout()
        assert page.is_order_completed(), "Order không hoàn thành"
        msg = page.get_order_success_message()
        print(f"\n→ Kết quả: {msg}")

    def test_order_number_generated(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.do_full_checkout()
        order_num = page.get_order_number()
        print(f"\n→ Order number: {order_num}")
        assert order_num != "", "Không có order number"


class TestBillingAddress:

    def test_billing_valid_address(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.proceed_to_checkout()
        page.fill_billing_us_address()
        page.continue_billing()
        page.handle_shipping_address()
        url = page.get_url()
        print(f"\n→ URL sau billing: {url}")
        assert "checkout" in url.lower()

    def test_billing_address_saved_exists(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.proceed_to_checkout()
        from selenium.webdriver.common.by import By
        dropdown = logged_in_driver.find_elements(By.ID, "billing-address-select")
        assert len(dropdown) > 0, "Không có dropdown địa chỉ saved"
        print(f"\n→ Có {len(dropdown)} dropdown địa chỉ")


class TestShippingMethod:

    def test_shipping_methods_available(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.proceed_to_checkout()
        page.fill_billing_us_address()
        page.continue_billing()
        page.handle_shipping_address()

        # Chờ section shipping method active trước khi tìm
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        WebDriverWait(logged_in_driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#opc-shipping_method.active")
            )
        )

        # Tìm đúng selector trong section shipping_method
        methods = logged_in_driver.find_elements(
            By.CSS_SELECTOR, "#opc-shipping_method input[type='radio']"
        )
        print(f"\n→ Số shipping methods: {len(methods)}")
        assert len(methods) > 0, "Không có shipping method nào"

    def test_select_shipping_method(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.proceed_to_checkout()
        page.fill_billing_us_address()
        page.continue_billing()
        page.handle_shipping_address()
        page.select_shipping_method()
        page.continue_shipping_method()
        url = page.get_url()
        assert "checkout" in url.lower()
        print(f"\n→ URL sau shipping: {url}")


class TestPayment:

    def test_select_payment_method(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.proceed_to_checkout()
        page.fill_billing_us_address()
        page.continue_billing()
        page.handle_shipping_address()
        page.select_shipping_method()
        page.continue_shipping_method()
        page.select_payment_method()
        page.continue_payment_method()
        url = page.get_url()
        assert "checkout" in url.lower()
        print(f"\n→ URL sau payment: {url}")

    def test_fill_payment_info(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.proceed_to_checkout()
        page.fill_billing_us_address()
        page.continue_billing()
        page.handle_shipping_address()
        page.select_shipping_method()
        page.continue_shipping_method()
        page.select_payment_method()
        page.continue_payment_method()
        page.fill_payment_info()
        page.continue_payment_info()
        url = page.get_url()
        assert "checkout" in url.lower()
        print(f"\n→ URL sau payment info: {url}")


class TestOrderConfirmation:

    def test_confirm_order(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.do_full_checkout()
        assert page.is_order_completed()
        print(f"\n→ Order: {page.get_order_success_message()}")

    def test_order_in_history(self, logged_in_driver):
        add_product_to_cart(logged_in_driver)
        page = CheckoutPage(logged_in_driver)
        page.open_cart()
        page.do_full_checkout()

        import time
        time.sleep(2)

        page.navigate("https://demowebshop.tricentis.com/customer/orders")
        time.sleep(2)

        from selenium.webdriver.common.by import By

        # Tìm theo nút Details — mỗi order có 1 nút Details
        orders = logged_in_driver.find_elements(
            By.XPATH, "//a[contains(@href,'/customer/order/')]"
        )
        if not orders:
            # Fallback: tìm theo text "Order Number"
            orders = logged_in_driver.find_elements(
                By.XPATH, "//*[contains(text(),'Order Number')]"
            )

        print(f"\n→ Số orders tìm thấy: {len(orders)}")
        assert len(orders) > 0, "Không thấy order trong history"